import requests
from utils.logger import log_message
from utils.proxy import get_random_proxy
from utils.helpers import random_delay

def run_task(access_token, task, headers, proxies, base_url, delay_min, delay_max):
    url = f"{base_url}/verify"
    payload = {"activityId": task["id"]}
    auth_headers = headers.copy()
    auth_headers["Authorization"] = f"Bearer {access_token}"
    proxy = get_random_proxy(proxies)
    proxy_dict = {"http": proxy, "https": proxy} if proxy else {}
    
    try:
        response = requests.post(url, json=payload, headers=auth_headers, proxies=proxy_dict)
        if response.status_code == 200:
            log_message(f"タスク {task['title']} ({task['type']}) 実行しました", "success")
            random_delay(delay_min, delay_max)
            return True
        else:
            log_message(f"タスク {task['title']} ({task['type']}) 実行に失敗しました", "error")
            return False
    except Exception as e:
        log_message(f"タスク {task['title']} ({task['type']}) 実行中にエラー", "error")
        return False