from tkinter import ttk
import tkinter
__author__ = 'zz'


class VarGetMixin:
    def get(self):
        return self.var.get()


class VarSetMixin:
   def set(self, value):
       self.var.set(value=value)


class HelpTextMixin:
    def __init__(self, *args, **kwargs):
        self.help_text = kwargs.pop('help_text','')
        super().__init__(*args, **kwargs)


class CheckButton(HelpTextMixin, VarGetMixin, ttk.Checkbutton):
    def __init__(self, master, value=1, **kwargs):
        self.var = tkinter.IntVar(value=value)
        kwargs.update(variable=self.var)
        super().__init__(master, **kwargs)


class Entry(HelpTextMixin, VarGetMixin, ttk.Entry):
    def __init__(self, master, value='', **kwargs):
        self.var = tkinter.StringVar(value=value)
        kwargs.update(textvariable=self.var)
        super().__init__(master, **kwargs)


class NumberEntry(HelpTextMixin, VarGetMixin, ttk.Entry):
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


class Label(HelpTextMixin, VarGetMixin, VarSetMixin, ttk.Label):
    def __init__(self, master, value=None, **kwargs):
        self.var = tkinter.StringVar(value=value)
        kwargs.update(textvariable=self.var)
        super().__init__(master, **kwargs)



class BaseFrame(ttk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self._init()

    def _init(self):
        raise NotImplementedError
