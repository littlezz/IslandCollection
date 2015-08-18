import queue
from threading import Thread
import requests
from .analyzer import Analyzer, init_start_url
import threading
from collections import namedtuple
from .structurers import ThreadSafeSet, FilterableList
__author__ = 'zz'


_sentinel = object()
Task = namedtuple('Task', ['url', 'response_gt', 'max_page'])


def singleton(cls):
    _instance=None
    def wrapper(*args, **kwargs):
        nonlocal _instance
        if not _instance:
            _instance = cls(*args, **kwargs)
        return _instance
    return wrapper


@singleton
class Engine:
    def __init__(self, tasks=None, max_thread=8):
        # tasks should be a list of dict contain 'url', 'response_gt','max_page'
        self._init_tasks(tasks)
        self.max_thread = max_thread
        self._init()

    def _init(self):
        self._task_queue = queue.Queue()
        self._result_cache_queue = queue.Queue()
        self._busying = ThreadSafeSet()
        self._results = FilterableList()
        self._thread_tasks = []
        self._shutdown = False
        self._shutdown_lock = threading.Lock()
        self._result_lock = threading.Lock()
        self._queue_timeout = 1
        self._pre_work_running = False

    @property
    def is_running(self):
        return any(t.is_alive() for t in self._thread_tasks)

    @property
    def is_busy(self):
        if self._busying:
            return True
        else:
            return False

    @property
    def results(self):
        """
        :return: collect results which already pop in get_one_result method.
                when engine stop, it will return the whole results
        """
        if not self.is_running:
            while self.get_one_result():
                pass

        return self._results


    def _init_tasks(self, tasks):
        self.init_tasks = []
        simple  = tasks[0]

        if isinstance(simple, Task):
            for task in tasks:
                self.init_tasks.append(task._asdict())

        else:
            for task in tasks:
                self.init_tasks.append(task)

        for task in self.init_tasks:
            task['url'] = init_start_url(task['url'])


    def set_init_tasks(self, tasks):
        self._reset()
        self._init_tasks(tasks)

    def _reset(self):
        """
        reset the engine, re init the engine
        """
        if self.is_running:
            self.shutdown()

        self._init()




    def start(self):

        self._pre_work_running = True

        t = threading.Thread(target=self._generate_tasks)
        t.start()
        self._thread_tasks.append(t)

        self._pre_work_running = False

        for i in range(self.max_thread):
            t = Thread(target=self.worker)
            t.start()
            self._thread_tasks.append(t)


    def _generate_tasks(self):
        for task in self.init_tasks:
            url = task['url']
            response_gt = task['response_gt']
            max_page = task['max_page']
            # add the init task immediately to avoid main worker stop
            self.add_task(url, response_gt, max_page)
            r = self._fetch(url)
            a = Analyzer(r, max_page)
            while True:
                if self._shutdown:
                    return

                url = a.next_page(current_page_url=url)
                if not url:
                    break

                self.add_task(url, response_gt, max_page)


    def worker(self):
        try:
            while True:
                # data is Task object
                data = self._retrieve_task()
                if data is _sentinel:
                    self._task_queue.put(data)
                    return
                else:
                    url, response_gt, max_page = data

                # shutdown immediately
                if self._shutdown:
                    break
                self._busying.add(url)
                r = self._fetch(url)
                a = Analyzer(r, max_page)
                self._add_result(a.filter_divs(response_gt=response_gt))
                self._busying.remove(url)
        except BaseException as e:
            # TODO: log error
            print(type(e), e)
            raise e


    def shutdown(self, wait=True):
        with self._shutdown_lock:
            self._shutdown = True
            self._task_queue.put(_sentinel)

        if wait:
            for t in self._thread_tasks:
                t.join()


    def _retrieve_task(self):
        while True:
            try:
                t = self._task_queue.get(timeout=self._queue_timeout)
            except queue.Empty:
                self._detect_finish()
            else:
                return t

    def _detect_finish(self):
        if self._task_queue.empty() and not self.is_busy and not self._pre_work_running:
            self._task_queue.put(_sentinel)


    def _fetch(self, url):
        r = requests.get(url)
        return r

    def _add_result(self, results):
        for result in results:
            self._result_cache_queue.put(result)

    def add_task(self, url, response_gt, max_page):
        if not url:
            return

        t = Task(url, response_gt, max_page)
        self._task_queue.put(t)

    def get_one_result(self):
        """
        :return: result or None which does not  mean the engine is stop!
        """
        try:
            result = self._result_cache_queue.get_nowait()
        except queue.Empty:
            result = None

        if result:
            with self._result_lock:
                self._results.append(result)

        return result



engine = Engine()




