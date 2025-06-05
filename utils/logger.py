from termcolor import colored

def log_message(message, status):
    colors = {"success": "green", "error": "red", "info": "yellow"}
    print(colored(f"[{status.upper()}] {message}", colors[status.lower()]))