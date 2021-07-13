import threading
from alfonso_db import Currencies

def interval(func, time):

    e = threading.Event()
    while not e.wait(time):
        func(update=False)


interval(Currencies, 3600)