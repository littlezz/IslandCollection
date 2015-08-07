from tkinter import ttk
from gui.widgets import CheckButton, Entry, NumberEntry, BaseFrame

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


class FeetFrame(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.button = ttk.Button(self, text='Start!')
        self.button.grid(column=0, row=0)

    def set_button_command(self, command):
        self.button.configure(command=command)



class SideFrame(BaseFrame):
    def _init(self):
        self.add_button = ttk.Button(self, text='+', command=self.master.add_content_row)
        self.add_button.grid(column=0, row=0)


class ContentFrame(BaseFrame):
    def _init(self):
