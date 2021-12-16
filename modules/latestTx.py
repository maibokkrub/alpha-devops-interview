import click
import pandas as pd
from utils import fetch_contract_last_n_tx, get_verified_ERC20contract_instance

@click.command()
@click.argument('contract_address')
@click.argument('amount')
def get_latest_transactions(contract_address, amount):
    """
        Generate Latest N to a text file showing sender address, txHash, and decoded call data. 

    """
    
    contract = get_verified_ERC20contract_instance(contract_address)
    click.echo(f"[INFO] Fetching latest {amount} transactions -- newest to oldest")
    txs = fetch_contract_last_n_tx(contract_address, int(amount))
    # df = pd.read_csv('latestTX.csv')
    
    df = pd.DataFrame.from_records(txs)
    df.to_csv("latestTX.csv")
    #TODO: maybe we can do better?
    df = df[['from', 'hash', 'input']]
    df = df.join(df.apply( 
        lambda row: pd.Series(contract.decode_function_input(row['input']),index=['call_function', 'call_args']),
        result_type='expand',
        axis=1,
    ))
    df = df.drop(['input'], axis=1)
    print( df[['from', 'call_function']])
    df.to_csv(f'latestTXN-{contract_address}.csv', index=False)
