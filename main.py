#! python3

import click
from web3 import Web3

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
    click.echo("Initilizing modules")
    from modules.detail import detail
    cli.add_command(detail)


if __name__ == '__main__':
    initialize_modules()
    click.echo('========')
    cli()
