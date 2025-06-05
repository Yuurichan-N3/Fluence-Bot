import json
import os
from eth_account import Account
from utils.logger import log_message

def generate_wallet():
    account = Account.create()
    wallet_data = {
        "address": account.address,
        "private_key": account._private_key.hex()
    }
    return wallet_data

def save_wallet(wallet_data):
    if os.path.exists("data/wallets.json"):
        with open("data/wallets.json", "r") as file:
            wallets = json.load(file)
    else:
        wallets = []
    
    wallets.append(wallet_data)
    
    with open("data/wallets.json", "w") as file:
        json.dump(wallets, file, indent=4)
    
    log_message(f"ウォレットが保存されました: {wallet_data['address']}", "success")