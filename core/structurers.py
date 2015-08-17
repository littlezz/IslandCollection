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
        self.name, self.operator = self._split_clause(lp)
        self.value = rp

    def _split_clause(self, s):
        clauses = s.split('__')
        if len(clauses) == 1:
            return clauses[0], None
        else:
            return clauses[0], clauses[1]

    def find(self, data):
        """
        validate the data if satisfy this lookup
        :return: True or False
        """


class FilterableList(UserList):
    # todo: rewrite filter method
    # def filter(self, **kwargs):
    #     ret = self.__class__()
    #
    #     for i in self.data:
    #         if all(getattr(i, name)==value for name, value in kwargs.items()):
    #             ret.append(i)
    #
    #     return ret
    def filter(self, **kwargs):
        """
        :param kwargs: one key-value pattern
        :return:filterable list
        """
        ret = self.__class__()

        assert len(kwargs) == 1, 'filter method accept one  lookup per time'
        lookup = LookUp(**kwargs)

        for item in self.data:
            if lookup.find(item):
                ret.append(item)

        return ret
