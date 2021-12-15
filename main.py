#! python3

import click

# ETHER KEY 5VHZC7JW44R4KPP6PMXG9EQDB5SI1XZFJ9
# WEB3 INFURA PROJECT ID b252831e0c3b4d8b89eae0adee8e71f0

@click.group()
def cli():
    ''' CLI for Alpha Finance Interview '''

# def validate_configurations():
#     ''' Doc String '''
#     pass

def initialize_modules():
    """ 
        Initialize Modules with w3 connection

    """

    from modules.detail import detail
    cli.add_command(detail, name="detail")
    from modules.balanceOf import balanceOf
    cli.add_command(balanceOf, name="balanceOf")
    from modules.watchTx import watchTx
    cli.add_command(watchTx, name="watchTx")
    from modules.latestTx import get_latest_transactions
    cli.add_command(get_latest_transactions, name="latestTx")
    from modules.topHolders import topHolders
    cli.add_command(topHolders, name="topHolder")


if __name__ == '__main__':
    initialize_modules()
    cli()
