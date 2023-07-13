import time

from rbxapi.utils import get_csrf_token
import requests
from colorama import Fore, Style

csrf_token = get_csrf_token()



def is_username_taken(username, proxy, accept_not_appropriate):
    global csrf_token

    session = requests.session()
    session.headers.update({
        "x-csrf-token": csrf_token
    })

    if proxy is not False:
        session.proxies = {
            "http": proxy,
            "https": proxy
        }

    try:
        response = session.post("https://auth.roblox.com/v1/usernames/validate", json={"username": username, "context": "Signup", "birthday": "1971-08-03T04:00:00.000Z"})
    except:
        print(Fore.YELLOW + "Checking status failed for \""+username+"\", retrying..." + Fore.RESET)
        time.sleep(0.5)
        return is_username_taken(username, proxy, accept_not_appropriate)
    if response.status_code == 200:
        json = response.json()
        if json["code"] == 0 and json["message"] == "Username is valid.":
            return False
        elif json["code"] == 2 and accept_not_appropriate:
            return False
        elif json["code"] == 1 and json["message"] == "Username is already in use":
            return True
        return True
    elif response.status_code == 403:
        csrf_token = get_csrf_token()

        return is_username_taken(username, proxy, accept_not_appropriate)
