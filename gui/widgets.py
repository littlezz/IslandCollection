from tkinter import ttk
import tkinter
__author__ = 'zz'


class VarGetMixin:
    def get(self):
        return self.var.get()


class CheckButton(VarGetMixin, ttk.Checkbutton):
    def __init__(self, master, **kwargs):
        self.var = tkinter.IntVar()
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




class UrlSelectColumnFrame(ttk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.check_button = CheckButton(self)
        self.url_text = Entry(self)
        self.response_num_text = NumberEntry(self)
        self.max_page_text = NumberEntry(self)
        self.delete_button = ttk.Button(self, text='Delete')

        self.check_button.grid(column=0, row=0)
        self.url_text.grid(column=1, row=0)
        self.response_num_text.grid(column=2, row=0)
        self.max_page_text.grid(column=3, row=0)
        self.delete_button.grid(column=4, row=0)


