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
    register_operator = ('in', 'gt', 'lt', 'eq', 'abs_eq')
    DEFAULT_OPERATOR = 'eq'

    def __init__(self, **kwargs):
        lp, rp = kwargs.popitem()
        self.lookup_name, self.operator = self._split_clause(lp)
        self.lookup_value = rp

        assert self.operator in self.register_operator, 'Do not support operator:{} '.format(self.operator)

    def _split_clause(self, s):
        clauses = s.split('__')
        if len(clauses) == 1:

            return clauses[0], self.DEFAULT_OPERATOR
        else:
            return clauses[0], clauses[1]

    def find(self, data):
        """
        validate the data if satisfy this lookup
        :return: True or False
        """
        assert hasattr(data, self.lookup_name), 'data has no {} attribute'.format(self.lookup_name)
        target = getattr(data, self.lookup_name)

        return getattr(self, '_op_{}'.format(self.operator))(target)


    def _op_in(self, target):
        return self.lookup_value in target


    def _op_gt(self, target):
        target = int(target)
        lookup_value =int(self.lookup_value)
        return target > lookup_value

    def _op_lt(self, target):
        return not self._op_gt(target)

    def _op_eq(self, target):
        if isinstance(self.lookup_value, bool):
            return bool(target) == self.lookup_value
        else:
            return self._op_abs_eq(target)

    def _op_abs_eq(self, target):
        return target == self.lookup_value


class FilterableList(UserList):

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
