from bs4 import BeautifulSoup
import requests


def get_csrf_token():
    soup = BeautifulSoup(requests.get("https://roblox.com").content, "html.parser")
    return soup.find("meta", attrs={"name": "csrf-token"})["data-token"]
