import click
from web3 import Web3
import json
import requests

def clean_address(address):
    return Web3.toChecksumAddress(address)

def get_connection(): 
    """ 
        Initilze RPC connection to ETH network
        Return an connection instance

    """

    click.echo("[INFO] Connecting to RPC")
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/b252831e0c3b4d8b89eae0adee8e71f0'))
    if w3.isConnected: 
        click.echo(" > Connected")
        return w3 
    click.echo("[ERROR] Web3 RPC Connection Error")


def get_ERC20contract_instance(contract_address): 
    """ 
        Connect and return a web3 contract instance

    """

    connection = get_connection()
    contract_address = clean_address(contract_address)
    click.echo("[INFO] Reading ABI")
    with open('./abis/ERC20.json') as f:
        abi = json.load(f)
    
    try:
        return connection.eth.contract(contract_address, abi=abi)
    except Exception as e: 
        print(e) 

def get_latest_block(): 
    return get_connection().eth.get_block_number()

def fetch_contract_genesis_block(contract_address): 
    contract_address = clean_address(contract_address)

    params = { 
        "module"    :'account',
        "action"    :'txlistinternal',
        "startblock": 0, 
        "endblock"  : get_latest_block(), 
        "page"      : 1, 
        "offset"    : 1,
        "sort"      : 'asc', 
        "address"   : contract_address, 
        "apikey"    : '5VHZC7JW44R4KPP6PMXG9EQDB5SI1XZFJ9', 
    }

    result = requests.get('https://api.etherscan.io/api', params).json()
    click.echo("[INFO] Fetching Genesis block from etherscan")
    return result['result'][0]['blockNumber']


def fetch_contract_last_n_tx(contract_address, amount, startblock=0, endblock=get_latest_block()): 
    contract_address = clean_address(contract_address)

    #TODO: Loop over, parallelize quries
    if amount > 9999: 
        raise ValueError("Etherscan limit 10,000 per requests")

    params = { 
        "module"    : 'account',
        "action"    : 'txlist',
        "startblock": startblock, 
        "endblock"  : endblock, 
        "page"      : 1, 
        "offset"    : amount,
        "sort"      : 'desc', 
        "address"   : contract_address, 
        "apikey"    : '5VHZC7JW44R4KPP6PMXG9EQDB5SI1XZFJ9', 
    }

    result = requests.get('https://api.etherscan.io/api', params).json()
    click.echo("[INFO] Fetching Genesis block from etherscan")
    return result['result']

async def transfer_events_aggregator(): 
    pass

def fetch_contract_transfer_events(contract_address, page=1,startblock=0, endblock=get_latest_block()): 
    contract_address = clean_address(contract_address)
    params = { 
        "module"    : 'account',
        "action"    : 'tokentx',
        "startblock": startblock, 
        "endblock"  : endblock, 
        "page"      : page, 
        "offset"    : 10000,
        "sort"      : 'asc', 
        "contractaddress": contract_address, 
        "apikey"    : '5VHZC7JW44R4KPP6PMXG9EQDB5SI1XZFJ9', 
    }
    click.echo(f"[INFO] Fetching Transfer Events from etherscan -- block {startblock} to {endblock}")
    result = requests.get('https://api.etherscan.io/api', params)
    print(result.url)
    return (result.json())['result']

def generate_explorer_link(tx_hash): 
    return f"https://etherscan.io/tx/{tx_hash}"