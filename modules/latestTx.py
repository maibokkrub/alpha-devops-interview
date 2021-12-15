import click
from utils import fetch_contract_last_n_tx, generate_explorer_link

@click.command()
@click.argument('contract_address')
@click.argument('amount')
def get_latest_transactions(contract_address, amount):
    """
        Subscribe Tx from the contract_address in watching mode and constantly output the url link to etherscan.io
    
    """
    
    # contract = get_ERC20contract_instance(contract_address)
    click.echo(f"[INFO] Fetching latest {amount} transactions -- newest to oldest")
    txs = fetch_contract_last_n_tx(contract_address, int(amount))
    
    for i,tx in enumerate(txs):
        print(f'[{i}]')
        print(f"  From:  {tx['from']}")
        print(f"  To:    {tx['to']}")
        print(f"  Value: {tx['value']}")
        print(f"  \t{generate_explorer_link(tx['hash'])}")
