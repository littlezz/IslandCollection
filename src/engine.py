import queue
from threading import Thread
import requests

__author__ = 'zz'


_sentinel = object()

class Engine:
    def __init__(self, urls=None, max_thread=8):
        assert urls
        self.max_thread = max_thread
        self._con_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self._thread_tasks = []
        self.is_run = False

    def start(self):
        for i in range(self.max_thread):
            t = Thread(target=self.run)
            t.start()
            self._thread_tasks.append(t)

        self.is_run = True



    def run(self):
        while True:
            data = self._con_queue.get()
            if data is _sentinel:
                self._con_queue.put(data)
                break

            self.fetch(data)
#             TODO



