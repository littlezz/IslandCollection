import threading
from collections import UserList
__author__ = 'zz'



class ThreadSafeSet(set):
    def __init__(self, *args, **kwargs):
        self._add_lock = threading.Lock()
        super().__init__(*args, **kwargs)

    def add(self, *args, **kwargs):
        with self._add_lock:
            return super().add(*args, **kwargs)


class FilterableList(UserList):
    # todo: rewrite filter method
    def filter(self, **kwargs):
        ret = []
        for i in self.data:
            if all(getattr(i, name)==value for name, value in kwargs.items()):
                ret.append(i)

        return ret
