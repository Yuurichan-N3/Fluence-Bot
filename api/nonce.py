import requests
from utils.logger import log_message
from utils.proxy import get_random_proxy

def get_nonce(wallet_address, headers, proxies, base_url):
    url = f"{base_url}/auth/nonce"
    payload = {"walletAddress": wallet_address}
    proxy = get_random_proxy(proxies)
    proxy_dict = {"http": proxy, "https": proxy} if proxy else {}
    
    try:
        response = requests.post(url, json=payload, headers=headers, proxies=proxy_dict)
        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                log_message("ノンスを取得しました", "success")
                return data["data"]["nonce"]
            else:
                log_message("ノンスの取得に失敗しました", "error")
                return None
        else:
            log_message("ノンスの取得に失敗しました", "error")
            return None
    except Exception as e:
        log_message("ノンス取得中にエラー", "error")
        return None