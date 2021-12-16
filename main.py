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
    """ 
    Initialize Modules with w3 connection

    """
    # from modules.detail import detail
    # cli.add_command(detail, name="detail")
    from modules.balanceOf import balanceOf
    cli.add_command(balanceOf, name="balanceOf")
    # from modules.watchTx import watchTx
    # cli.add_command(watchTx, name="watchTx")
    # from modules.latestTx import get_latest_transactions
    # cli.add_command(get_latest_transactions, name="latestTx")
    # from modules.topHolders import topHolders
    # cli.add_command(topHolders, name="topHolder")


if __name__ == '__main__':
    load_dotenv()
    validate_configurations()
    initialize_modules()
    cli()
