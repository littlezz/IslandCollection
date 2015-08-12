from tkinter import ttk
import tkinter
import webbrowser
__author__ = 'zz'


class VarGetSetMixin:
    def get(self):
        return self.var.get()

    def set(self, value):
       self.var.set(value=value)




class StringVarMixin(VarGetSetMixin):
    def __init__(self, *args, **kwargs):
        value = kwargs.pop('value', None)
        self.var = tkinter.StringVar(value=value)
        kwargs.update(textvariable=self.var)
        super().__init__(*args, **kwargs)


class HelpTextMixin:
    def __init__(self, *args, **kwargs):
        self.help_text = kwargs.pop('help_text','')
        super().__init__(*args, **kwargs)


class HyperMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind('<1>', self._click)

    def _click(self, event):
        webbrowser.open_new(self._get_url())

    def _get_url(self):
        raise NotImplementedError





class CheckButton(HelpTextMixin, VarGetSetMixin, ttk.Checkbutton):
    def __init__(self, master, value=1, **kwargs):
        self.var = tkinter.IntVar(value=value)
        kwargs.update(variable=self.var)
        super().__init__(master, **kwargs)


class Button(HelpTextMixin, ttk.Button):
    pass


class Entry(HelpTextMixin, StringVarMixin, ttk.Entry):
    pass


class NumberEntry(HelpTextMixin, VarGetSetMixin, ttk.Entry):
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


class InfoLabel(HelpTextMixin, StringVarMixin, ttk.Label):
    pass


class HyperLabel(HyperMixin, ttk.Label):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(foreground='blue', cursor='hand2')

    def _get_url(self):
        return self['text']


class BaseFrame(ttk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self._init()

    def _init(self):
        raise NotImplementedError
