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



class LookUp:
    def __init__(self, **kwargs):
        lp, rp = kwargs.popitem()
        self.name, self.operator = self.split_clause(lp)
        self.value = rp

    def split_clause(self, s):
        clauses = s.split('__')
        if len(clauses) == 1:
            return clauses[0], None
        else:
            return clauses[0], clauses[1]



class FilterableList(UserList):
    # todo: rewrite filter method
    def filter(self, **kwargs):
        ret = []
        for i in self.data:
            if all(getattr(i, name)==value for name, value in kwargs.items()):
                ret.append(i)

        return ret
