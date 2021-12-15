import click
from time import sleep
from utils import generate_explorer_link, get_ERC20contract_instance, get_connection

@click.command()
@click.argument('contract_address')
def watchTx(contract_address):
    """
        Subscribe Tx from the contract_address in watching mode and constantly output the url link to etherscan.io
    
    """
    
    w3 = get_connection()
    contract_address = w3.toChecksumAddress(contract_address)
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
    
