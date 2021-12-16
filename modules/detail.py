import click

@click.command()
@click.argument('contract_address')
def detail(contract_address):
    """
        Show name, symbol and decimals of the contract CONTRACT_ADDRESS
    
    """
    from utils import get_ERC20contract_instance

    contract = get_ERC20contract_instance(contract_address)
    name     = contract.functions.name().call()
    symbol   = contract.functions.symbol().call()
    decimals = contract.functions.decimals().call()

    print(f'Contract Address: {contract_address}')
    print(f'Token Name: {name}')
    print(f'Token Symbol: {symbol}')
    print(f'Token Decimals: {decimals}')