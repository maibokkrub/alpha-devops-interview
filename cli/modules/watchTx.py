import click
from time import sleep

@click.command()
@click.argument('contract_address')
def watchTx(contract_address):
    """
        Subscribe Tx from the contract_address in watching mode 
        and constantly output the url link to etherscan.io
    
    """
    from utils import clean_address, generate_explorer_link, get_connection

    w3 = get_connection(True)
    contract_address = clean_address(contract_address)
    click.echo(f"[INFO] -- Watching tx on {contract_address}, press Ctrl+C to exit --")

    try: 
        tx_filter = w3.eth.filter({
            "address"   : contract_address, 
            "fromBlock" : 'latest', 
            "removed"   : 'true', 
        })

        while True:
            temp = set()
            for event in tx_filter.get_new_entries():
                tx_hash = event['transactionHash'].hex()
                if tx_hash not in temp:
                    print(f" \t{generate_explorer_link(tx_hash)}")
                    temp.add(tx_hash)
            sleep(2)

        
    except KeyboardInterrupt: 
        click.echo("[INFO] > Exit Signal Received")
    
