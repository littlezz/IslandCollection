from tkinter import ttk
from gui.widgets import CheckButton, Entry, NumberEntry, BaseFrame
from gui.layouts import BaseMainFrameLayout
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


class FootFrame(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.button = ttk.Button(self, text='Start!')
        self.button.grid(column=0, row=0)

    def set_button_command(self, command):
        self.button.configure(command=command)



class SideFrame(BaseFrame):
    def _init(self):
        self.add_button = ttk.Button(self, text='+')
        self.add_button.grid(column=0, row=0)


class ContentFrame(BaseFrame):
    def _init(self):
        self.row_num = 0

    def add_content_row(self):
        row = UrlSelectColumnFrame(self)
        row.grid(column=0, row=self.row_num)
        self.row_num += 1


class MainFrame(BaseMainFrameLayout):

    def _init(self):
        self.content_frame = ContentFrame(self)
        self.side_frame = SideFrame(self)
        self.foot_frame = FootFrame(self)

        self.side_frame.add_button.configure(command=self.content_frame.add_content_row)

