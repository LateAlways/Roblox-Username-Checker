import re
import time


class Proxy:
    def __init__(self, proxy):
        self.ip = proxy.split(":")[0]
        self.port = proxy.split(":")[1]

        self.last_used = time.time()

    def is_ip_valid(self):
        if self.ip.count(".") != 3:
            return False
        else:
            for i in self.ip.split("."):
                try:
                    if 0 <= int(i) <= 255:
                        return True
                except ValueError:
                    return False

            return False

    def is_port_valid(self):
        try:
            if 0 <= int(self.port) <= 65535:
                return True
        except ValueError:
            return False

        return False

    def get_full_name(self):
        return "http://"+self.ip + ":" + self.port

    def is_valid(self):
        return True

    def get_last_used(self):
        return self.last_used

    def use(self):
        self.last_used = time.time()
