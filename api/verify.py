import requests
from web3 import Web3
from eth_account.messages import encode_defunct
from utils.logger import log_message
from utils.proxy import get_random_proxy

def verify_wallet(wallet_address, nonce, private_key, headers, proxies, base_url):
    web3 = Web3()
    message = encode_defunct(text=nonce)
    signature = web3.eth.account.sign_message(message, private_key=private_key).signature.hex()
    
    url = f"{base_url}/auth/verify"
    payload = {
        "walletAddress": wallet_address,
        "signature": signature
    }
    proxy = get_random_proxy(proxies)
    proxy_dict = {"http": proxy, "https": proxy} if proxy else {}
    
    try:
        response = requests.post(url, json=payload, headers=headers, proxies=proxy_dict)
        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                log_message("ウォレットの認証に成功しました", "success")
                return data["data"]["accessToken"]
            else:
                log_message("ウォレットの認証に失敗しました", "error")
                return None
        else:
            log_message("ウォレットの認証に失敗しました", "error")
            return None
    except Exception as e:
        log_message("認証中にエラー", "error")
        return None