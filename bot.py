import yaml
import json
import os
import time
import importlib.util
from utils.logger import log_message
from utils.wallet import generate_wallet, save_wallet
from utils.proxy import load_proxies
from api.nonce import get_nonce
from api.verify import verify_wallet
from api.tasks import get_task_ids
from api.referral import apply_referral
from tasks.runner import run_task
from termcolor import colored

def check_dependencies():
    required_modules = ["requests", "web3", "eth_account", "termcolor", "yaml"]
    missing = []
    for module in required_modules:
        if importlib.util.find_spec(module) is None:
            missing.append(module)
    if missing:
        log_message(f"依存モジュールが不足しています: {', '.join(missing)}", "error")
        return False
    return True

def print_banner():
    print(colored("╔══════════════════════════════════════════════╗", "cyan"))
    print(colored("║       🌟 FLUENCE BOT - Automated Tasks       ║", "cyan"))
    print(colored("║   Automate your Pointless API interactions!  ║", "cyan"))
    print(colored("║  Developed by: https://t.me/sentineldiscus   ║", "cyan"))
    print(colored("╚══════════════════════════════════════════════╝", "cyan"))
    print()

def load_config():
    try:
        config_path = os.path.join("config", "settings.yaml")
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)
        headers_path = os.path.join("config", "headers.json")
        with open(headers_path, "r") as file:
            headers = json.load(file)
        return config, headers
    except Exception as e:
        log_message(f"コンフィグの読み込みエラー: {str(e)}", "error")
        return None, None

def main():
    if not check_dependencies():
        return
    
    config, headers = load_config()
    if not config or not headers:
        return
    
    proxies = load_proxies()
    
    print_banner()
    
    referral_code = input(colored("Masukkan kode referral: ", "yellow"))
    try:
        num_referrals = int(input(colored("Masukkan jumlah referral: ", "yellow")))
    except ValueError:
        log_message("紹介人数は数字で入力してください", "error")
        return
    
    for i in range(num_referrals):
        try:
            wallet = generate_wallet()
            
            nonce = get_nonce(wallet["address"], headers, proxies, config["api"]["base_url"])
            if not nonce:
                continue
            
            access_token = verify_wallet(wallet["address"], nonce, wallet["private_key"], headers, proxies, config["api"]["base_url"])
            if not access_token:
                continue
            
            save_wallet(wallet)
            
            if not apply_referral(access_token, referral_code, headers, proxies, config["api"]["base_url"]):
                continue
            
            task_ids = get_task_ids(wallet["address"], headers, proxies, config["api"]["base_url"])
            for task in task_ids:
                if not run_task(access_token, task, headers, proxies, config["api"]["base_url"], config["delay"]["task_min"], config["delay"]["task_max"]):
                    continue
            
            log_message(f"紹介の処理が完了しました", "success")
            time.sleep(config["delay"]["iteration"])
        
        except Exception as e:
            log_message(f"紹介処理中にエラー: {str(e)}", "error")
            continue
    
    log_message("すべての処理が完了しました", "success")

if __name__ == "__main__":
    main()
