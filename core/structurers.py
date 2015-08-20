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
    register_operator = ('contain', 'gt', 'lt', 'eq', 'abs_eq')
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
        obj_value = getattr(data, self.lookup_name)

        return getattr(self, '_op_{}'.format(self.operator))(obj_value)

    def _op_contain(self, obj_value):
        return self.lookup_value in obj_value

    def _op_gt(self, obj_value):
        obj_value = int(obj_value)
        lookup_value = int(self.lookup_value)
        return obj_value > lookup_value

    def _op_lt(self, obj_value):
        return not self._op_gt(obj_value)

    def _op_eq(self, obj_value):
        if isinstance(self.lookup_value, bool) or isinstance(obj_value, bool):
            return bool(obj_value) == bool(self.lookup_value)
        else:
            return self._op_abs_eq(obj_value)

    def _op_abs_eq(self, obj_value):
        return obj_value == self.lookup_value


class FilterableList(UserList):

    def filter(self, **kwargs):
        """
        :param kwargs: one key-value pattern
        :return:filterable list
        """
        if not kwargs:
            return self.all()

        assert len(kwargs) == 1, 'filter method accept one  lookup per time'

        lookup = LookUp(**kwargs)
        ret = self.__class__()

        for item in self.data:
            if lookup.find(item):
                ret.append(item)

        return ret

    def all(self):
        return self[:]


class ResultInfo:
    # __slots__ = ('text', 'link', 'response_num', 'image_url')

    def __init__(self, text, link, response_num, image_url=None, image_fp=None):
        self.text = text
        self.link = link
        self.response_num = response_num
        self.image_url = image_url
        self.image_fp = image_fp

    @property
    def has_image(self):
        return True if self.image_url or self.image_fp else False


    def as_dict(self):
        return self.__dict__