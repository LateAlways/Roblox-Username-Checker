import os
import time

from rbxapi.utils import get_csrf_token
import requests
from colorama import Fore, Style

csrf_token = get_csrf_token()

def get_available_usernames(usernames, proxy):
    global csrf_token

    if proxy is not False:
        print(proxy)
        os.environ["HTTP_PROXY"] = proxy
        os.environ["HTTPS_PROXY"] = proxy

    try:
        response = requests.post("https://users.roblox.com/v1/usernames/users", headers={"x-csrf-token": csrf_token}, json={"usernames": usernames, "excludeBannedUsers": False})
    except KeyboardInterrupt:
        exit()
    except Exception:
        for user in usernames:
            print(Fore.YELLOW + "Checking status failed for \"" + user + "\", retrying..." + Fore.RESET)
        time.sleep(0.5)
        return get_available_usernames(usernames, proxy)
    if response.status_code == 200:
        json = response.json()
        taken = []
        non_taken = []
        for user in usernames:
            found = False
            for valid_user in json["data"]:
                if valid_user["requestedUsername"] == user:
                    found = True
                    taken.append(user)
                    break
            if not found:
                non_taken.append(user)

        return [non_taken, taken]
    elif response.status_code == 403:
        csrf_token = get_csrf_token()

        return get_available_usernames(usernames, proxy)
    elif response.status_code == 429:
        for user in usernames:
            print(Fore.YELLOW + "Checking status failed for \"" + user + "\", retrying... (RATELIMIT)" + Fore.RESET)

        time.sleep(15)
        return get_available_usernames(usernames, proxy)
