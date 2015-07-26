import queue
from threading import Thread
import requests
from .analyzer import Analyzer
import threading
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
        self._shutdown_lock = threading.Lock()

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
        try:
            while True:
                # data is (url, response_gt)
                data = self._task_queue.get()
                if data is _sentinel:
                    self._task_queue.put(data)
                    return
                else:
                    url, response_gt = data

                r = self.fetch(url)
                a = Analyzer(r)
                self.add_result(a.filter_divs(response_gt=response_gt))
                self.add_task(a.next_page(), response_gt)

        except BaseException as e:
            # TODO: log error
            print(type(e), e)


    def shutdown(self):
        with self._shutdown_lock:
            self._running = False
            self._task_queue.put(_sentinel)

        for t in self._thread_tasks:
            t.join()

    def fetch(self, url):
        pass

    def add_result(self, results):
        pass

    def add_task(self, url, response_gt):
        pass








