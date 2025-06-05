import requests
from utils.logger import log_message
from utils.proxy import get_random_proxy

def get_task_ids(wallet_address, headers, proxies, base_url):
    url = f"{base_url}/points/{wallet_address}"
    proxy = get_random_proxy(proxies)
    proxy_dict = {"http": proxy, "https": proxy} if proxy else {}
    
    try:
        response = requests.get(url, headers=headers, proxies=proxy_dict)
        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                task_ids = []
                activities = data["data"]["activities"]
                for category in ["daily", "earning", "oneTime", "pointless"]:
                    for task in activities.get(category, []):
                        task_ids.append({
                            "id": task["id"],
                            "title": task["title"],
                            "type": category
                        })
                log_message(f"タスクIDを取得しました: {[task['id'] for task in task_ids]}", "success")
                return task_ids
            else:
                log_message("タスクIDの取得に失敗しました", "error")
                return []
        else:
            log_message("タスクIDの取得に失敗しました", "error")
            return []
    except Exception as e:
        log_message("タスクID取得中にエラー", "error")
        return []