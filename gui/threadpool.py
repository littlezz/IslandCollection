import threading
import queue
from concurrent.futures import thread
import atexit
__author__ = 'zz'

# shutdown program immediately
atexit.unregister(thread._python_exit)

thread_pool = thread.ThreadPoolExecutor(4)

# class ThreadPoll:
#     def __init__(self, max_workers=4):
#         self.max_workers = max_workers
#         self.threads = []
#         self.queue = queue.Queue()
#         self.start()
#
#     def start(self):
#         for i in range(self.max_workers):
#             t = threading.Thread(target=self.work)
#             t.daemon = True
#             t.start()
#
#     def work(self):
#         while True:
#             fn = self.queue.get()
#             if fn == None:
#                 return
#             fn()
#
#     def submit(self, fn):
#         self.queue.put(fn)
#
#     def shutdown(self, wait=False):
#         self.queue.put(None)


