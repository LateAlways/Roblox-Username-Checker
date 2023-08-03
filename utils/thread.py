import ctypes
import time
from threading import Thread

queue = []
running = True
pausing = False


print_comm = print

def print(msg):
    queue.append(msg)


def wait():
    global pausing
    pausing = True
    time.sleep(1)
    pausing = False


def update_title(available, taken):
    ctypes.windll.kernel32.SetConsoleTitleW("Roblox Username Generator | By: LateAlways | Available: " + str(available) + " | Taken: " + str(taken))


def update(available, taken):
    global queue
    if len(queue) > 0:
        print_comm(queue[0])
        queue.pop(0)

    update_title(available, taken)


def launch(function, threads):
    for i in range(threads):
        Thread(target=function).start()
