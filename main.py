from colorama import init, Fore
from proxies.proxymanager import ProxyManager
from rbxapi.auth import get_available_usernames
from usergen.base.UsernameGeneration import UsernameGeneration
from usergen.randomletters import RandomLetters
import utils.thread as threading

from threading import Thread
import json
from discord_webhook import DiscordWebhook, DiscordEmbed
import os


config = json.load(open("config.json", "r"))

THREADS = config["threads"]
init()
os.system("cls")

proxy_manager: ProxyManager = ProxyManager()
if config["proxies"] is not False:
    proxy_manager.load_from_file(config["proxies"])
username_generator: UsernameGeneration
if config["username_generation_algorithm"] == "RandomLetters":
    username_generator = RandomLetters()

available = 0
taken = 0

def run():
    global available
    global taken
    while threading.running:
        while threading.pausing:
            pass

        usernames = username_generator.get_next_users(config["batch"])
        available_users, non_available = get_available_usernames(usernames, proxy_manager.get_proxy().get_full_name() if len(proxy_manager.http_proxies) > 0 else False)
        available_str = ""
        for username in available_users:
            print("[" + Fore.GREEN + "+" + Fore.RESET + "] " + Fore.GREEN + username + " is not taken! | https://roblox.com/" + Fore.RESET)
            available += 1
            available_str += username + "\n"

            # discord webhook
            if config["webhook"] is not False:
                webhook = DiscordWebhook(url=config["webhook"])
                embed = DiscordEmbed(title="Username sniped!", description="Username: " + username + "\nLink: https://roblox.com/", color=242424)
                webhook.add_embed(embed)
                webhook.execute()
            threading.wait()

        with open(config["username_save_file"], "a") as file:
            file.write(available_str)
            file.close()

        for username in non_available:
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
