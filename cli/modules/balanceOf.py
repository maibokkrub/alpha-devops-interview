import click

@click.command()
@click.argument('contract_address')
@click.argument('target_address')
def balanceOf(contract_address, target_address):
    """
        Show the balanceOf target_address on the contract_address 
        in decimals format
    
    """
    from web3.main import Web3
    from utils import get_ERC20contract_instance
    contract = get_ERC20contract_instance(contract_address)

    click.echo("[INFO] Fetching Data")
    decimals    = 10 ** contract.functions.decimals().call()
    symbol      = contract.functions.symbol().call()
    target_address = Web3.toChecksumAddress(target_address)
    raw_balance = contract.functions.balanceOf(target_address).call()

    click.echo(f"========")
    click.echo(f"Target Account: {target_address}")
    click.echo(f"Balance: {raw_balance/decimals} {symbol}")