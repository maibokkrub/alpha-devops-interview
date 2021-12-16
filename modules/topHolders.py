
import csv
import click
from time import sleep, time_ns
from utils import fetch_contract_transfer_events, get_ERC20contract_instance
import pandas as pd 

@click.command()
@click.argument('contract_address')
@click.argument('amount')
def topHolders(contract_address, amount):
    """
        Subscribe Tx from the contract_address in watching mode and constantly output the url link to etherscan.io
    
    """
    
    # click.echo(f"[INFO] Fetching latest {amount} transactions -- newest to oldest")
    click.echo("[INFO] Fetching Contract Data")
    contract = get_ERC20contract_instance(contract_address)
    decimals    = contract.functions.decimals().call()
    symbol      = contract.functions.symbol().call()

    holders = {}
    current_page = 1
    results = fetch_contract_transfer_events(contract_address)

    while results:
        click.echo(f"[INFO] Parsing Page {current_page}")
        #TODO: Init , Dead wallet
        for transfer in results:
            tx_from = transfer['from']
            tx_to   = transfer['to'] 
            tx_val  = int(transfer['value'])
            if tx_from not in holders:
                holders[tx_from] = 0 
            if tx_to not in holders: 
                holders[tx_to] = 0
            holders[tx_from] -= tx_val
            holders[tx_to] += tx_val
    
        current_page += 1
        sleep(0.3) #Rate Limit
        results = fetch_contract_transfer_events(contract_address, page=1, startblock=int(results[-1]['blockNumber'])+1)

    # For reading from csv
    # with open(f'allholders-{contract_address}.csv', 'r') as csv_file:  
    #     reader = csv.reader(csv_file)
    #     for line in reader: 
    #         holders[line[0]] = int(line[1])
        
    df = pd.DataFrame.from_dict(holders, orient='index', columns=[symbol])
    df.reset_index(level=0, inplace=True)
    df.rename(columns={'index':'Address'}, inplace=True)
    df.to_csv(f'allholders-{contract_address}.csv')
    top_holders = df.sort_values(by=[symbol], ascending=False)[:int(amount)]
    top_holders[symbol] = top_holders[symbol] / 10**decimals 
    
    print(f"Top {amount} holders for {symbol}")
    pd.options.display.float_format = ('{:.0'+str(decimals)+'f}').format
    print(top_holders)
