import queue
from threading import Thread
import requests
from .analyzer import Analyzer

__author__ = 'zz'


_sentinel = object()


class Engine:
    def __init__(self, tasks=None, max_thread=8):
        # tasks should be a dict, eg, {url: response_gt}
        self.url_tasks = tasks
        self.max_thread = max_thread
        self._task_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self._thread_tasks = []
        self._running = False

    @property
    def is_run(self):
        return self._running

    def start(self):
        for i in range(self.max_thread):
            t = Thread(target=self.run)
            t.start()
            self._thread_tasks.append(t)

        self._running = True



    def run(self):
        while True:
            url = self._task_queue.get()
            if url is _sentinel:
                self._task_queue.put(url)
                break

            r = self.fetch(url)
            a = Analyzer(r)
            self.add_result(a.filter_divs(response_gt=self.url_tasks[r.url]))
            self.add_task(a.next_page())


    def stop(self):
        self._running = False
        self._task_queue.put(_sentinel)

    def fetch(self, url):
        pass

    def add_result(self, results):
        pass

    def add_task(self, url):
        pass







