import os
import random
from utils.logger import log_message

def load_proxies():
    proxy_file = "data/proxy.txt"
    if os.path.exists(proxy_file):
        with open(proxy_file, "r") as file:
            proxies = [line.strip() for line in file if line.strip()]
        if proxies:
            log_message(f"プロキシを読み込みました: {len(proxies)}個", "info")
            return proxies
        else:
            log_message("プロキシリストが空です", "error")
            return []
    else:
        log_message("proxy.txtが見つかりません", "error")
        return []

def get_random_proxy(proxies):
    return random.choice(proxies) if proxies else None