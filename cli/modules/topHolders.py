import click
import pandas as pd 
from time import sleep

@click.command()
@click.argument('contract_address')
@click.argument('amount')
def topHolders(contract_address, amount):
    """
        Get current top holders for a given ERC20 contract.

        Description: 
            Fetch the etherscan api from startblock to endblock.
            Then replay the paginated results to calculate the latest balance for each holder. 
            We skip the last block in page N to refetch in N+1 to prevent paginated results cut out.

        Output Files: 
            allholders-{contract_address}.csv               Contains all holders data 
            topHolders-{amount}-{contract_address}.csv      Contains only top AMOUNT holders
    """
    from utils import fetch_contract_transfer_events, get_ERC20contract_instance

    click.echo("[INFO] Fetching Contract Data")
    contract  = get_ERC20contract_instance(contract_address)
    decimals  = contract.functions.decimals().call()
    symbol    = contract.functions.symbol().call()

    holders = {}
    current_page = 1
    results = fetch_contract_transfer_events(contract_address, startblock=0)

    while True:
        click.echo(f"[INFO] Parsing Page {current_page}")
        next_block = results[-1]['blockNumber']
        # Replay All Transfer Events
        for transfer in results:
            if transfer['blockNumber'] == next_block:
                break
            tx_from = transfer['from']
            tx_to   = transfer['to'] 
            tx_val  = int(transfer['value'])
            if tx_from not in holders:
                holders[tx_from] = 0 
            if tx_to not in holders: 
                holders[tx_to]   = 0
            holders[tx_from] -= tx_val
            holders[tx_to] += tx_val

        # Offset is always set to 10000 if not last page
        if len(results) < 10000: 
            break 

        current_page += 1
        sleep(0.3)  #Rate Limit
        results = fetch_contract_transfer_events(contract_address, startblock=next_block)
    
    #TODO: fix messy code
    df = pd.DataFrame.from_dict(holders, orient='index', columns=[symbol])
    df.reset_index(level=0, inplace=True)
    df.rename(columns={'index':'Address'}, inplace=True)
    df.to_csv(f'allholders-{contract_address}.csv', index=False)
    top_holders = df.sort_values(by=[symbol], ascending=False)[:int(amount)]
    top_holders.to_csv(f'topHolders-{amount}-{contract_address}.csv', index=False)
    top_holders[symbol] = top_holders[symbol] / 10**decimals 
    
    print(f"Top {amount} holders for {symbol}")
    pd.options.display.float_format = ('{:.0'+str(decimals)+'f}').format   #Set Float alignment
    print(top_holders)
