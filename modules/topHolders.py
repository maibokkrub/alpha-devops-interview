from collections import Counter
import enum
import click
from time import sleep, time_ns
from utils import fetch_contract_transfer_events, get_ERC20contract_instance

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
    decimals    = 10 ** contract.functions.decimals().call()
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
            tx_val  = int(transfer['value']) / decimals
            if tx_from not in holders:
                holders[tx_from] = 0 
            if tx_to not in holders: 
                holders[tx_to] = 0
            holders[tx_from] -= tx_val
            holders[tx_to] += tx_val
    
        current_page += 1
        sleep(0.3) #Rate Limit
        results = fetch_contract_transfer_events(contract_address, page=1, startblock=int(results[-1]['blockNumber'])+1)
    
    counts_sorted = sorted(holders.values())

    fp = open('topholders-'+contract_address,'w')
    fp.writelines(holders)

    amount = int(amount)
    top_holders  = []
    shown_count  = -1
    prev = -1 
    # round_winner = set()
    for winning_value in reversed(counts_sorted):
        if prev != winning_value:
            if shown_count >= amount: 
                break
            winner = (key for key, value in holders.items() if value == winning_value)
            top_holders.append((prev, [k for k in winner]))
            prev = winning_value
            # round_winner = set()
        holders[winner] = -1
        shown_count += 1

    
    for entry in top_holders[1:]: 
        #Todo: cleanup to decimals
        print(entry[0], symbol, )
        for p in entry[1]: 
            print(f'  {p}')

