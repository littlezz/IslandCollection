from tkinter import ttk
from gui.widgets import CheckButton, NumberEntry, BaseFrame, InfoLabel, Button, UrlEntry
from gui.layouts import BaseMainFrameLayout
from core.database import Tasks
from core import analyzer
from core.engine import engine
__author__ = 'zz'


class UrlSelectColumnFrame(ttk.Frame):
    def __init__(self, master=None, id=None, url='', response_gt=None, max_page=None, is_using=True, **kw):
        super().__init__(master, **kw)
        self.database_id = id
        self.check_button = CheckButton(self, value=is_using, help_text='是否启用')
        self.url_text = UrlEntry(self, width=50, value=url, help_text='url!!!!')
        self.response_num_text = NumberEntry(self, width=5, value=response_gt, help_text='最小相应数')
        self.max_page_text = NumberEntry(self, width=5, value=max_page, help_text='最大搜索页数')
        self.delete_button = Button(self, text='Delete', command=self.delete, help_text='删除')

        self.check_button.grid(column=0, row=0)
        self.url_text.grid(column=1, row=0)
        self.response_num_text.grid(column=2, row=0)
        self.max_page_text.grid(column=3, row=0)
        self.delete_button.grid(column=4, row=0)

        for w in self.children.values():
            w.bind('<Enter>', self.show_help_text)

    def get_as_dict(self):
        ret = {
            'url': self.url_text.get(),
            'response_gt': self.response_num_text.get(),
            'max_page': self.max_page_text.get(),
            'is_using': self.check_button.get(),
            'id': self.database_id,
        }
        return ret

    def info_is_using(self):
        """
        :return: If Checkbutton is pressed
        """
        return True if self.check_button.get() else False

    def delete(self):
        Tasks.delete_by_id(self.database_id)
        self.destroy()

    def show_help_text(self, event):
        help_text = event.widget.help_text
        self.master.set_info(help_text)


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
        self.add_button.grid(column=0, row=0, sticky='NW')
        self.save_button = ttk.Button(self, text='save')
        self.save_button.grid(column=0, row=1, sticky='NW')

        self.info_label = InfoLabel(self, width=20, wraplength=150)
        self.info_label.grid(column=0, row=2)

        # ttk.Frame(self,width=100).grid(column=0, row=3)

    def set_info(self, info):

        self.info_label.set(info)


class ContentFrame(BaseFrame):
    def _init(self):
        # self.column_names = UrlSelectColumnFrame(self)
        # self.column_names.grid(column=0, row=0)

        # [w.destroy() for w in self.column_names.winfo_children()]
        #
        # _Label = partial(ttk.Label, self.column_names)
        # _Label(text='URL', width=20).grid(column=0, row=0, sticky='W')
        # _Label(text='Response Number').grid(column=1, row=0)
        # _Label(text='Max Page').grid(column=2, row=0)

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

        tasks = Tasks.get_all()

        # if there is no tasks in database , show one line
        if not tasks.exists():
            self.add_content_row()
            return

        for t in tasks:
            # TODO:fix this
            t.pop('create_time')
            self.add_content_row(**t)


    def save(self):
        """
        save content info
        :return:
        """
        for index, row in enumerate(self.children.values()):
            task = row.get_as_dict()
            if self.validate_task(row, task):
                is_success = Tasks.create_or_update_data(task)
                # TODO: resolve not success
                if not is_success:
                    info = 'fail'
                else:
                    info='successful!'
                self.set_info(info)
                if not is_success:
                    break
            else:
                print(index)
                break

    def set_info(self, info):
        self.master.set_info(info)

    def validate_task(self, widget, task):
        url = task.get('url')
        status_code = analyzer.validate_url(url)
        if status_code != 0:

            widget.configure(style="wrong.TFrame")
            if status_code == 1:
                self.set_info('input right url')
            if status_code == 2:
                self.set_info('island not support!')

            return False
        else:
            # widget
            pass
            return True


class MainFrame(BaseMainFrameLayout):

    def _init(self):
        self.content_frame = ContentFrame(self)
        self.side_frame = SideFrame(self)
        self.foot_frame = FootFrame(self)

        self.side_frame.add_button.configure(command=self.content_frame.add_content_row)
        self.side_frame.save_button.configure(command=self.content_frame.save)
        self.foot_frame.button.configure(command=self.next_frame)
        self._make_style()

    def next_frame(self):
        # validate there at least have one task
        if any(row.info_is_using() for row in self.content_frame.children.values()):
            super().next_frame()
        else:
            self.set_info('no task select!')

    def _make_style(self):
        style = ttk.Style(self)
        style.configure('wrong.TFrame', background='red')

    def set_info(self, info):
        self.side_frame.set_info(info)

    def on_change(self):
        tasks = [row.get_as_dict() for row in self.content_frame.children.values() if row.info_is_using()]
        engine.set_init_tasks(tasks)
        engine.start()