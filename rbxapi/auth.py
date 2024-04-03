import os
import time

from rbxapi.utils import get_csrf_token
import requests
from colorama import Fore, Style

csrf_token = get_csrf_token()

def get_available_usernames(usernames, proxy):
    global csrf_token

    if proxy is not False:
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

def validate_username(username, proxy):
    global csrf_token
    if proxy is not False:
        os.environ["HTTP_PROXY"] = proxy
        os.environ["HTTPS_PROXY"] = proxy
        
    r = requests.post("https://auth.roblox.com/v1/usernames/validate", headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "x-csrf-token": csrf_token
    }, json={"username":username,"context":"Signup","birthday":"1971-08-03T04:00:00.000Z"}).json()
    if "error" in r:
        return False
    if "errors" in r and errors[0]["message"] == "Token Validation Failed":
        csrf_token = get_csrf_token()
        return validate_username(username, proxy)
    if "code" in r and r["code"] == 0:
        return True
    else:
        return False
    
