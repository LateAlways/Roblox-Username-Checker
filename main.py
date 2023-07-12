from colorama import init, Fore
from proxies.proxymanager import ProxyManager
from rbxapi.auth import is_username_taken
from usergen.base.UsernameGeneration import UsernameGeneration
from usergen.randomletters import RandomLetters
import utils.thread as threading

from threading import Thread
import json
import os


config = json.load(open("config.json", "r"))

THREADS = config["Threads"]
init()
os.system("cls")

proxy_manager: ProxyManager = ProxyManager()
if config["Proxied"] is True:
    proxy_manager.load_from_file(config["Proxy File"])
username_generator: UsernameGeneration
if config["Username Generation Algorithm"] == "RandomLetters":
    username_generator = RandomLetters()

available = 0
taken = 0
TAKEN = True

def run():
    global available
    global taken
    while threading.running:
        while threading.pausing:
            pass

        username = username_generator.get_next_user()
        status = is_username_taken(username, proxy_manager.get_proxy().get_full_name() if len(proxy_manager.http_proxies) > 0 else False, False)
        if status is not TAKEN:
            print("[" + Fore.GREEN + "+" + Fore.RESET + "] " + Fore.GREEN + username + " is not taken! | https://roblox.com/register" + Fore.RESET)
            available += 1
            threading.wait()
        else:
            threading.print("[" + Fore.RED + "-" + Fore.RESET + "] " + Fore.RED + username + " is taken." + Fore.RESET)
            taken += 1


threading.launch(run, THREADS)

while True:
    try:
        threading.update(available, taken)
    except KeyboardInterrupt:
        threading.running = False
        print("Cleaning up...")
        break