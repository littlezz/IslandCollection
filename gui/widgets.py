from tkinter import ttk
import tkinter
__author__ = 'zz'


class VarGetMixin:
    def get(self):
        return self.var.get()


class CheckButton(VarGetMixin, ttk.Checkbutton):
    def __init__(self, master, value=1, **kwargs):
        self.var = tkinter.IntVar(value=value)
        kwargs.update(variable=self.var)
        super().__init__(master, **kwargs)


class Entry(VarGetMixin, ttk.Entry):
    def __init__(self, master, **kwargs):
        self.var = tkinter.StringVar()
        kwargs.update(textvariable=self.var)
        super().__init__(master, **kwargs)


class NumberEntry(VarGetMixin, ttk.Entry):
    def __init__(self, master, value=None, **kwargs):
        super().__init__(master, **kwargs)
        self.var = tkinter.IntVar(value=value)
        vcmd = (self.register(self.validating), '%S')

        cf = dict()
        cf.update(textvariable=self.var)
        cf.update(validatecommand=vcmd)
        cf.update(validate='key')
        self.configure(**cf)


    def validating(self, text):
        allow = '0123456789'
        if all(c in allow for c in text):
            return True
        return False




