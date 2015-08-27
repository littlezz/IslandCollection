from .. import widgets
from .. import layouts
import queue
from tkinter import ttk
import tkinter as tk
from PIL import Image
from core.structurers import FilterableList, ResultInfo
from gui.threadpool import thread_pool
from core.engine import engine
__author__ = 'zz'




class RowFrame(ttk.Frame):
    _width = 600
    _height = 200
    def __init__(self, master, **kwargs):
        self.image_url = kwargs.pop('image_url', None)
        self.image_fp = kwargs.pop('image_fp', None)
        self.text = kwargs.pop('text', '')
        self.link = kwargs.pop('link', '')
        self.response_num = int(kwargs.pop('response_num', 0))
        super().__init__(master, **kwargs)


        self.image_frame = widgets.ImageFrame(self, image_url=self.image_url, image_fp=self.image_fp)

        self.link_label = widgets.HyperLabel(self, text=self.link, link=self.link, cursor='hand2', foreground='blue')
        self.text_label = ttk.Label(self, text=self.text, width=44, wraplength=345)
        self.response_num_label = ttk.Label(self, text='response ' + str(self.response_num))

        self.image_frame.grid(column=0, row=0, rowspan=2)
        self.link_label.grid(column=1, row=0, sticky='NW')
        self.response_num_label.grid(column=2, row=0, sticky='NW')
        self.text_label.grid(column=1, row=1, sticky='NW', columnspan=2)

        self.separator = ttk.Separator(self, orient=tk.HORIZONTAL)
        self.separator.grid(column=0, row=2, columnspan=2, sticky='we', pady=7 , padx=25)

    @property
    def has_image(self):
        return True if self.image_url or self.image_fp else False


class FootFrame(widgets.BaseFrame):
    def _init(self):
        self.button = widgets.Button(self, text='Back', help_text='back')
        self.progressbar = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=400, mode='determinate')

        self.progressbar.grid(column=0, row=0, sticky='we')
        self.button.grid(column=0, row=1)
    def set_button_command(self, command):
        self.button.configure(command=command)

    def progressbar_start(self):
        self.progressbar.start()

    def progressbar_stop(self):
        self.progressbar.stop()


class SideFrame(widgets.BaseFrame):
    def _init(self):

        self.image_only = widgets.CheckButton(self, text='image only',
                                              value=False,
                                              command=self.image_only_command)

        self.cb = widgets.ExtraDataComboBox(self,
                                            values_pair=(('link contain', 'link__contain'),
                                                         ('内容包含', 'text__contain'),
                                                         ('响应数大于', 'response_num__gt'),
                                                         ('响应数小于', 'response_num__lt')
                                                         ),
                                            help_text='filter type', state='readonly', width=10)

        self.entry = widgets.Entry(self, help_text='filter args')
        self.submit = widgets.Button(self, text='filter', command=self.submit_filter)

        self.image_only.grid(column=0, row=0, sticky='NW')
        self.cb.grid(column=0, row=1)
        self.entry.grid(column=1, row=1)
        self.submit.grid(column=0, row=2, columnspan=1)

        self.reset_button = widgets.Button(self, text='reset', command=self._on_reset)
        self.reset_button.grid(column=1, row=2)


    def _on_reset(self):
        self.entry.set('')
        self.cb.set('')
        self.image_only.set(0)
        self.master.clear_filter()

    def submit_filter(self):

        kw = {}

        if self.image_only.get():
            kw.update(has_image=self.image_only.get())

        filter_type = self.cb.get()
        args = self.entry.get()

        kw.update({filter_type: args})
        self.master.do_filter(**kw)

    def image_only_command(self):
        if self.image_only.get():
            self.master.do_filter(has_image=True)
        else:
            self.master.clear_filter()


class ContentFrame(widgets.ScrollbarCanvasMixin, widgets.BaseFrame):
    canvas_height = 570
    canvas_width = 550

    def _init(self):


        self._once_init()

    def _once_init(self):
        self.results = FilterableList()
        self.filter_kwargs = dict()
        self._queue = queue.Queue()

        self.rows = 0


    def show_results(self, results):
        """
        generate the results
        :parameter results: instance RawFrame list
        """
        for r in results:
            self.show_one_result(r)


    def show_one_result(self, result:RowFrame):

        result.grid(column=0, row=self.rows)
        self.rows += 1

    def add_new_result(self, result:ResultInfo):
        row = RowFrame(self.frame, **result.as_dict())

        # 检测当前的row是否符合过滤规则
        if FilterableList([row]).filter(**self.filter_kwargs):
            self.show_one_result(row)

        self.results.append(row)





    def test(self):
        import time
        for i in range(50):
            print(i)
            im = Image.open('gui/images_test/1.png')
            result = {
                'image_url': "http://h.nimingban.com/Public/Upload/image/2015-08-18/55d2bff64c32f.jpg",
                'text': 'the'+str(i) + '0123456789'*20,
                'link': 'http://www.baidu.com',
                'response_num':30,
            }
            m = i % 3
            if m ==0:
                result = ResultInfo(**result)
            elif m==1:
                result.pop('image_url')
                result['image_fp'] = im
                result = ResultInfo(**result)
            else:
                result.pop('image_url')
                result = ResultInfo(**result)

            self._queue.put(result)

        self._queue.put(None)

    def retrieve_result_from_engine(self):
        import time

        self.master.progressbar_start()

        while engine.is_running:
            result = engine.get_one_result()
            if result:
                self._queue.put(result)

            else:
                time.sleep(0.5)

        self._queue.put(None)
        self.master.progressbar_stop()

    def communicate_for_get_result(self):
        while True:
            try:
                result = self._queue.get_nowait()
                if result is None:
                    return

                self.add_new_result(result)
            except queue.Empty:
                break

        self.after(500, self.communicate_for_get_result)


    def do_filter(self, **kwargs):
        """
        pass nothing will clear the filter
        :param kwargs:
        :return:
        """

        self.filter_kwargs = kwargs
        results = self.results.all()

        for key, value in kwargs.items():
            results = results.filter(**{key: value})

        self.refresh_result_pannel()
        self.show_results(results)

    def clear_filter(self):
        self.do_filter()


    def refresh_result_pannel(self):
        for c in self.frame.winfo_children():
            c.grid_forget()

        self.rows = 0

    def clear(self):

        for c in self.frame.winfo_children():
            c.destroy()
        self._once_init()



class MainFrame(layouts.BaseMainFrameLayout):
    def _init(self):
        self.content_frame = ContentFrame(self)
        self.side_frame = SideFrame(self)
        self.foot_frame = FootFrame(self)

        self.foot_frame.button.configure(command=self.previous_frame)


    def do_filter(self, **kwargs):
        self.content_frame.do_filter(**kwargs)

    def clear_filter(self):
        self.content_frame.clear_filter()

    def on_show(self, pass_data):

        self.content_frame.clear()
        self.thread = thread_pool.submit(self.content_frame.retrieve_result_from_engine)
        self.content_frame.after(200, self.content_frame.communicate_for_get_result)

    def on_change(self):
        engine.shutdown(wait=False)

    def progressbar_start(self):
        self.foot_frame.progressbar_start()

    def progressbar_stop(self):
        self.foot_frame.progressbar_stop()