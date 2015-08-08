from tkinter import ttk
from gui.widgets import CheckButton, Entry, NumberEntry, BaseFrame, Label
from gui.layouts import BaseMainFrameLayout
from core import database
from functools import partial
__author__ = 'zz'




class UrlSelectColumnFrame(ttk.Frame):
    def __init__(self, master=None, id=None, url='', response_gt=None, max_page=None, is_using=True, **kw):
        super().__init__(master, **kw)
        self.database_id = id
        self.check_button = CheckButton(self, value=is_using)
        self.url_text = Entry(self, width=50, value=url)
        self.response_num_text = NumberEntry(self, width=5, value=response_gt)
        self.max_page_text = NumberEntry(self, width=5, value=max_page)
        self.delete_button = ttk.Button(self, text='Delete', command=self.delete)

        self.check_button.grid(column=0, row=0)
        self.url_text.grid(column=1, row=0)
        self.response_num_text.grid(column=2, row=0)
        self.max_page_text.grid(column=3, row=0)
        self.delete_button.grid(column=4, row=0)

    def get_as_dict(self):
        ret = {
            'url': self.url_text.get(),
            'response_gt': self.response_num_text.get(),
            'max_page': self.max_page_text.get(),
            'is_using': self.check_button.get(),
            'id':self.database_id,
        }
        return ret

    def delete(self):
        database.delete_by_id(self.database_id)
        self.destroy()


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
        self.save_button = ttk.Button(self, text='save')
        self.save_button.grid(column=0, row=1)

        self.info_label = Label(self)
        self.info_label.grid(column=0, row=2)

    def set_info(self, info):
        if not info:
            info = 'fail'
        else:
            info='successful!'
        self.info_label.set(info)




class ContentFrame(BaseFrame):
    def _init(self):
        self.row_num = 0
        self.init_list()

    def add_content_row(self, **kwargs):
        row = UrlSelectColumnFrame(self, **kwargs)
        row.grid(column=0, row=self.row_num)
        self.row_num += 1

    def init_list(self):
        """
        show database records
        :return:None
        """

        tasks = database.get_all()

        for t in tasks:
            # TODO:fix this
            t.pop('create_time')
            self.add_content_row(**t)


    def save(self, send_info):
        """
        save content info
        :return:
        """
        for _, row in self.children.items():
            task = row.get_as_dict()
            is_success = database.create_or_update_data(task)
            # TODO: resolve not success
            send_info(is_success)
            if not is_success:
                break


class MainFrame(BaseMainFrameLayout):

    def _init(self):
        self.content_frame = ContentFrame(self)
        self.side_frame = SideFrame(self)
        self.foot_frame = FootFrame(self)

        self.side_frame.add_button.configure(command=self.content_frame.add_content_row)

        _save_send_info = partial(self.content_frame.save, send_info=self.side_frame.set_info)
        self.side_frame.save_button.configure(command=_save_send_info)

