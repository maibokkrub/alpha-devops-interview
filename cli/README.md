# CLI

This is the first task for the `Blockchain-DevOps` Interview.
The package can be run under virtual environments, or a docker image.

## Requirements 
- Python 3.10 with pip
- Click 
- Web3py
- Pandas 

## Setting Up 
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install.

```bash
pip install -r requirements.txt
```

## Usage

```bash 
./main.py COMMAND [ARGS]
```

```
Usage: main.py [OPTIONS] COMMAND [ARGS]...

  CLI for Alpha Finance Interview

Options:
  --help  Show this message and exit.

Commands:
  balanceOf  Show the balanceOf target_address on the contract_address in...
  detail     Show name, symbol and decimals of the contract CONTRACT_ADDRESS
  latestTx   Generate Latest N to a text file showing sender address,...
  topHolder  Get current top holders for a given ERC20 contract.
  watchTx    Subscribe Tx from the contract_address in watching mode and...
```
---


### `balanceOf <CONTRACT_ADDRESS> <TARGET_ADDRESS>`
Show the balanceOf target_address on the contract_address in decimals format. 
```bash
./main.py balanceOf 0xB8c77482e45F1F44dE1745F52C74426C631bDD52 0xf977814e90da44bfa03b6295a0616a897441acec
```
Result:
```
[INFO] Connecting to RPC
 > Connected
[INFO] Connecting to RPC
 > Connected
[INFO] Connecting to RPC
 > Connected
[INFO] Reading local ERC20 ABI
[INFO] Fetching Data
========
Target Account: 0xF977814e90dA44bFA03b6295A0616a897441aceC
Balance: 4500000.0 BNB
```


### `detail <CONTRACT_ADDRESS>`
Show name, symbol and decimals of the contract CONTRACT_ADDRESS
```bash
./main.py detail 0xB8c77482e45F1F44dE1745F52C74426C631bDD52  
```

Result: 
```
[INFO] Connecting to RPC
 > Connected
[INFO] Connecting to RPC
 > Connected
[INFO] Connecting to RPC
 > Connected
[INFO] Reading local ERC20 ABI
Contract Address: 0xB8c77482e45F1F44dE1745F52C74426C631bDD52
Token Name: BNB
Token Symbol: BNB
Token Decimals: 18
```

### `latestTx <CONTRACT_ADDRESS> <AMOUNT> `
Generate Latest N to a text file
```bash 
./main.py latestTx 0xdac17f958d2ee523a2206206994597c13d831ec7 5  
```
The generated file is named as a csv file at `latestTX-<CONTRACT_ADDRESS>.csv`.

### `topHolder <CONTRACT_ADDRESS> <AMOUNT>`
Get current top holders for a given ERC20 contract.
```bash 
./main.py topHolder 0xdac17f958d2ee523a2206206994597c13d831ec7 5  
```
The generated file is named as a csv file at `topHolders-<CONTRACT_ADDRESS>.csv`.

Another file containing all holder values is also available at `allHolders-<CONTRACT_ADDRESS>.csv`.

### `watchTx <CONTRACT_ADDRESS>`
Subscribe Tx from the contract_address in watching mode and outputs a link to block explorer (etherscan).

```
./main.py watchTx 0xdac17f958d2ee523a2206206994597c13d831ec7                                             ─╯
```
Result: 
```
[INFO] Connecting to RPC
 > Connected
[INFO] Connecting to RPC
 > Connected
[INFO] Connecting to RPC
 > Connected
[INFO] -- Watching tx on 0xdAC17F958D2ee523a2206206994597C13D831ec7, press Ctrl+C to exit --
        https://etherscan.io/tx/0x90a66dbc1ca856ba2109d439af2e81884ccfc0c3a0396d26ec5a16d8511e17d8
        https://etherscan.io/tx/0xc66da29b109d868f46d351ee891e22fc43ec0d20980bbe724a15978b7b4efeec
     
... 
   
\^C[INFO] > Exit Signal Received
```

---

### Known issues
- Python import executes the module when it was imported causing multiple `Connecting to RPC` to show when start. (Does not effect functionality)