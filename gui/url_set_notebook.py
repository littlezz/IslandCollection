from tkinter import ttk
from gui.widgets import CheckButton, Entry, NumberEntry

__author__ = 'zz'




class UrlSelectColumnFrame(ttk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.check_button = CheckButton(self)
        self.url_text = Entry(self, width=50)
        self.response_num_text = NumberEntry(self, width=5)
        self.max_page_text = NumberEntry(self, width=5)
        self.delete_button = ttk.Button(self, text='Delete', command=self.destroy)

        self.check_button.grid(column=0, row=0)
        self.url_text.grid(column=1, row=0)
        self.response_num_text.grid(column=2, row=0)
        self.max_page_text.grid(column=3, row=0)
        self.delete_button.grid(column=4, row=0)


# TODO:fuck
class NoteFrame(ttk.Frame):
    def __init__(self, master, **kwargs):
        self.tot = 1
        super().__init__(master, **kwargs)
        self._f = ttk.Frame(self, width=500)
        self._f.grid(column=0, row=1, columnspan=5)
        ttk.Frame(self,width=500).grid(column=0, row=0, columnspan=5)
        add_button = ttk.Button(self, text='add', command=self.add_child)
        add_button.grid(column=6, row=0, sticky='NE')

    def add_child(self):
        u = UrlSelectColumnFrame(self._f)
        u.grid(column=0, row=self.tot)
        self.tot += 1
