#! python3

import click
from dotenv import load_dotenv
from os import getenv

@click.group()
def cli():
    ''' CLI for Alpha Finance Interview '''

def validate_configurations():
    ''' Validates if the env file is correctly loaded '''
    REQUIRED_FIELDS = [ 
        'ALPHA_CLI_RPC_URL', 
        'ALPHA_CLI_ETHERSCAN_KEY', 
        'ALPHA_CLI_ETHERSCAN_URL'
    ]
    for item in REQUIRED_FIELDS: 
        if not getenv(item): 
            print("[ERROR] CANNOT LOAD env for " + item)
            exit(400)

def initialize_modules():
    from modules import detail, balanceOf, watchTx, latestTx, topHolders
    cli.add_command(detail.detail, name="detail")
    cli.add_command(balanceOf.balanceOf, name="balanceOf")
    cli.add_command(watchTx.watchTx, name="watchTx")
    cli.add_command(latestTx.get_latest_transactions, name="latestTx")
    cli.add_command(topHolders.topHolders, name="topHolder")

if __name__ == '__main__':
    load_dotenv()
    validate_configurations()
    initialize_modules()
    try:
        cli()
    except Exception as e : 
        click.echo(e)
