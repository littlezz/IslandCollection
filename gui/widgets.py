from tkinter import ttk
import tkinter
__author__ = 'zz'


class CheckButton(ttk.Checkbutton):
    def __init__(self, master, **kwargs):
        self.var = tkinter.IntVar()
        kwargs.update(variable=self.var)
        super().__init__(master, **kwargs)

    def get(self):
        return self.var.get()

class Entry(ttk.Entry):
    def __init__(self, master, **kwargs):
        self.var = tkinter.StringVar()
        kwargs.update(textvariable=self.var)
        super().__init__(master, **kwargs)


class UrlSelectColumnFrame(ttk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.check_button = CheckButton(self)
        self.url_text = Entry(self, text='url')
        self.response_num_text = Entry(self, text='response')
        self.max_page_text = Entry(self, text='max page')
        self.delete_button = ttk.Button(self, text='Delete')

        self.check_button.grid(column=0, row=0)
        self.url_text.grid(column=1, row=0)
        self.response_num_text.grid(column=2, row=0)
        self.max_page_text.grid(column=3, row=0)
        self.delete_button.grid(column=4, row=0)


