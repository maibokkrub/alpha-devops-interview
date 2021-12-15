import click
from web3 import Web3
import json

def get_connection(): 
    """ 
    Initilze RPC connection to ETH network
    Return an connection instance
    """
    click.echo("Connecting to RPC")
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/b252831e0c3b4d8b89eae0adee8e71f0'))
    if w3.isConnected: 
        click.echo("Connected")
        return w3 
    click.echo("Web3 RPC Connection Error")


def get_ERC20contract_instance(contract_address): 
    """ 
    Connect and return a web3 contract instance
    """
    connection = get_connection()
    with open('./abis/ERC20.json') as f:
        abi = json.load(f)
    
    try: 
        return connection.eth.contract(contract_address, abi=abi)
    except Exception as e: 
        print(e) 
