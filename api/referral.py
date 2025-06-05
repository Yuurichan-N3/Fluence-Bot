import requests
from utils.logger import log_message
from utils.proxy import get_random_proxy

def apply_referral(access_token, referral_code, headers, proxies, base_url):
    url = f"{base_url}/referrals/apply"
    payload = {"referralCode": referral_code}
    auth_headers = headers.copy()
    auth_headers["Authorization"] = f"Bearer {access_token}"
    proxy = get_random_proxy(proxies)
    proxy_dict = {"http": proxy, "https": proxy} if proxy else {}
    
    try:
        response = requests.post(url, json=payload, headers=auth_headers, proxies=proxy_dict)
        if response.status_code == 200:
            log_message("紹介コードを適用しました", "success")
            return True
        else:
            log_message("紹介コードの適用に失敗しました", "error")
            return False
    except Exception as e:
        log_message("紹介コード適用中にエラー", "error")
        return False