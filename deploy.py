import json

from web3 import Web3
from solcx import compile_standard, install_solc

import os
from dotenv import load_dotenv
load_dotenv()

with open("./SmartContractDemo.sol", "r") as file:
    smart_contract_demo_file = file.read()

print("SmartContractDemo.sol : ")
print("_________________________")
print(smart_contract_demo_file)
print("_________________________\n")

install_solc("0.6.0")

# Solidity source code
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SmartContractDemo.sol" : { "content" : smart_contract_demo_file }},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi","metadata","evm.bytecode","evm.sourceMap"]
                }
            }
        }
    },
    solc_version="0.6.0",
)

with open("compiled_code.json","w") as file:
    json.dump(compiled_sol,file)

# get bytecode
bytecode = compiled_sol["contracts"]["SmartContractDemo.sol"]["SmartContractDemo"]["evm"]["bytecode"]["object"]

#  get abi
abi  = compiled_sol["contracts"]["SmartContractDemo.sol"]["SmartContractDemo"]["abi"]

# for connecting to ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
chain_id = 1337
my_address =  "0x5793Fd9F071A58E257f0978d853F5aeed4Af036e"
private_key = os.getenv("PRIVATE_KEY")
# private_key = "0x_________________________________________"

# Create the contract in python
SmartContractDemo = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)

# Submit the transaction deplays the contract
transaction = SmartContractDemo.constructor().buildTransaction({
    "chainId": chain_id,
    "gasPrice": w3.eth.gas_price,
    "from": my_address,
    "nonce": nonce,
})

# Sign the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

print("Deploying Contract!")

tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

# Wait for the transaction to be mined, and get transaction receipt
print("Waiting for Transaction to finish...")
tx_receipt=w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Done! Contract Deployed to {tx_receipt.contractAddress} \n")


# Working with the contracts
smart_contract_demo = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# Calling function: numberOfEntries()
print(f"\nInitial Number of Entries: {smart_contract_demo.functions.numberOfEntries().call()}")

# Calling function: store(string memory,string memory) and making state change
store_transaction = smart_contract_demo.functions.store("Naruto","10-10-1999").buildTransaction({
    "chainId": chain_id,
    "gasPrice": w3.eth.gas_price,
    "from":my_address,
    "nonce":nonce+1,
})
signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
signed_store_hash = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(signed_store_hash)

print(f"Final Stored Value {smart_contract_demo.functions.numberOfEntries().call()}")

# Calling function: retrieve(uint)
print(smart_contract_demo.functions.retrieve(0).call())