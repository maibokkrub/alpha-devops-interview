import click
from web3 import Web3
import json
import requests
from os import getenv

RPC_URL = getenv('ALPHA_CLI_RPC_URL')
API_URL = getenv('ALPHA_CLI_ETHERSCAN_URL')
API_KEY = getenv('ALPHA_CLI_ETHERSCAN_KEY')
EXPLORER_BASE = getenv('ALPHA_CLI_EXPLORER_URL')

##
##  Small Helpers
##

def clean_address(address):
    try:
        return Web3.toChecksumAddress(address)
    except Exception as e: 
        raise ValueError(f"[ERROR] CANNOT Clean Address {address}")

def get_latest_block():
    return get_connection(True).eth.get_block_number()

def generate_explorer_link(tx_hash):
    return f"{EXPLORER_BASE}/tx/{tx_hash}"


##
##  Web3 Helpers & Contract Related Utils
##

def get_connection(run=False): 
    """ 
        Initilzes a RPC connection to ETH network
        Returns an connection instance

    """

    click.echo("[INFO] Connecting to RPC")
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    if w3.isConnected: 
        click.echo(" > Connected")
        return w3 
    raise ValueError("[ERROR] Web3 RPC Connection Error")

def get_ERC20contract_instance(contract_address): 
    """ 
        Connect and return a web3.eth.contract instance
        using local basic ERC20 abi

    """
    if contract_address:
        connection = get_connection(True)
        contract_address = clean_address(contract_address)

        click.echo("[INFO] Reading local ERC20 ABI")
        with open('./abis/ERC20.json') as f:
            abi = json.load(f)
        try:
            return connection.eth.contract(contract_address, abi=abi)
        except Exception as e: 
            print(e) 

def fetch_contract_abi(contract_address):
    """ 
        Fetch ABI from etherscan if available

    """
    if contract_address:
        contract_address = clean_address(contract_address)
        params = { 
            "module"    : 'contract',
            "action"    : 'getabi',
            "address"   : contract_address, 
            "apikey"    : API_KEY, 
        }

        click.echo(f"[INFO] Fetching Contract ABI from etherscan...")
        result = requests.get(API_URL, params)
        result = (result.json())['result']
        if result != 'Contract source code not verified':
            return result
        raise ValueError('Invalid or Contract source code not verified')

def get_verified_ERC20contract_instance(contract_address): 
    """ 
        Connect and return a web3.eth.contract instance
        using an abi fetched from etherscan or else fallback 
        to local ERC20 ABI

    """
    if contract_address:
        connection = get_connection(True)
        contract_address = clean_address(contract_address)

        try:
            abi = fetch_contract_abi(contract_address)
        except ValueError as e:
            click.echo("[WARNING] ABI not available from etherscan, using local ERC20 abi")
            return get_ERC20contract_instance(contract_address)
        return connection.eth.contract(contract_address, abi=abi)



## 
##  Transaction Utils
##

def fetch_contract_last_n_tx(contract_address, amount, startblock=0, endblock=get_latest_block()):
    """ 
        Fetch transactions originated from a contract
        Ref: https://docs.etherscan.io/api-endpoints/accounts#get-a-list-of-normal-transactions-by-address

    """
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
        "apikey"    : API_KEY, 
    }

    click.echo("[INFO] Fetching latest mined transactions from etherscan...")
    result = requests.get(API_URL, params).json()
    return result['result']


def fetch_contract_transfer_events(contract_address, page=1,startblock=0, endblock=get_latest_block()):
    """ 
        Fetch all transfer events for a acontract
        Ref: https://docs.etherscan.io/api-endpoints/accounts#get-a-list-of-erc20-token-transfer-events-by-address

    """
    
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
        "apikey"    : API_KEY, 
    }

    click.echo(f"[INFO] Fetching Transfer Events from etherscan -- block {startblock} to {endblock}")
    result = requests.get(API_URL, params)
    print(result.url)
    return (result.json())['result']
