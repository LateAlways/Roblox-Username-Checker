from proxies.proxy import Proxy


class ProxyManager:
    def __init__(self):
        self.http_proxies = []
        self.http_use = {}

    def load_from_file(self, filename):
        with open(filename, "r") as f:
            for line in f.readlines():
                proxy = Proxy(line.strip())
                if proxy.is_valid():
                    self.add_proxy(proxy)

    def add_proxy(self, proxy: Proxy):
        if proxy.is_valid():
            self.http_proxies.append(proxy)

    def get_proxy(self) -> Proxy:
        self.http_proxies.sort(key=lambda x: x.get_last_used())
        self.http_proxies[0].use()

        return self.http_proxies[0]
