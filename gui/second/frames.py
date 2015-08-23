from .. import widgets
from .. import layouts
from tkinter import ttk
import tkinter as tk
from PIL import Image
from core.compat import IS_WINDOWS
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
        self.response_num = kwargs.pop('response_num', 0)
        super().__init__(master, **kwargs)


        self.image_frame = widgets.ImageFrame(self, image_url=self.image_url, image_fp=self.image_fp)

        self.link_label = widgets.HyperLabel(self, text=self.link, link=self.link, cursor='hand2', foreground='blue')
        self.text_label = ttk.Label(self, text=self.text, width=50, wraplength=400)

        self.image_frame.grid(column=0, row=0, rowspan=2)
        self.link_label.grid(column=1, row=0, sticky='NW')
        self.text_label.grid(column=1, row=1, sticky='NW')

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

        self.has_image = widgets.CheckButton(self, text='has image',
                                             command=lambda : self.master.do_filter(has_image=self.has_image.get()))

        self.cb = widgets.ExtraDataComboBox(self,
                                            values_pair=(('link contain', 'link__contain'), ('content contain', 'text__contain')),
                                            help_text='filter type')
        self.entry = widgets.Entry(self, help_text='filter args')
        self.submit = widgets.Button(self, text='filter', command=self.submit_filter)

        self.has_image.grid(column=0, row=0, sticky='NW')
        self.cb.grid(column=0, row=1)
        self.entry.grid(column=1, row=1)
        self.submit.grid(column=0, row=2, columnspan=2)

    def submit_filter(self):

        kw = {}
        kw.update(has_image=self.has_image.get())

        filter_type = self.cb.get()
        args = self.entry.get()

        kw.update({filter_type: args})
        self.master.do_filter(**kw)


class ContentFrame(widgets.BaseFrame):

    def _init(self):

        # FIXME: make the canvas auto fit the width
        # scrollable content
        self.canvas = tk.Canvas(self, height=600, width=600)
        self.frame = ttk.Frame(self.canvas)
        self.vbs = ttk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vbs.set)
        self.vbs.pack(side='right', fill='y')
        self.canvas.pack(side='left', fill='both', expand=True)
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw', tag='self.frame')
        self.frame.bind('<Configure>', self.on_frame_configure)
        self.canvas.bind_all('<MouseWheel>', self._on_mousewheel)
        self.results = FilterableList()
        self.filter_kwargs = dict()

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



    def on_frame_configure(self, e):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mousewheel(self, e):
        if IS_WINDOWS:
            self.canvas.yview_scroll(-int(e.delta/120), 'units')
        else:
            self.canvas.yview_scroll(-e.delta, 'units')

    def test(self):
        import time
        for i in range(50):
            print(i)
            im = Image.open('gui/images_test/1t.jpg')
            result = {
                'image_url': "http://h.nimingban.com/Public/Upload/image/2015-08-18/55d2bff64c32f.jpg",
                'text': 'the'+str(i) + '0123456789'*20,
                'link': 'http://www.baidu.com',
                'response_num':30,
            }
            m = i % 3
            if m ==0:
                result = ResultInfo(**result)
                self.add_new_result(result)
            elif m==1:
                result.pop('image_url')
                result['image_fp'] = im
                result = ResultInfo(**result)
                self.add_new_result(result)
            else:
                result.pop('image_url')
                result = ResultInfo(**result)
                self.add_new_result(result)
            time.sleep(0.5)

    def retrieve_result_from_engine(self):
        import time

        self.master.progressbar_start()

        while engine.is_running:
            result = engine.get_one_result()
            if result:
                self.add_new_result(result)
                time.sleep(0)
            else:
                time.sleep(0.5)

        self.master.progressbar_stop()


    def do_filter(self, **kwargs):

        self.filter_kwargs = kwargs
        results = self.results.all()

        for key, value in kwargs.items():
            results = results.filter(**{key: value})

        self.refresh_result_pannel()
        self.show_results(results)

    def refresh_result_pannel(self):
        for c in self.frame.winfo_children():
            c.grid_forget()

        self.rows = 0


class MainFrame(layouts.BaseMainFrameLayout):
    def _init(self):
        self.content_frame = ContentFrame(self)
        self.side_frame = SideFrame(self)
        self.foot_frame = FootFrame(self)

        self.foot_frame.button.configure(command=self.previous_frame)


    def do_filter(self, **kwargs):
        self.content_frame.do_filter(**kwargs)

    def on_show(self, pass_data):

        self.thread = thread_pool.submit(self.content_frame.retrieve_result_from_engine)

    def on_change(self):
        # TODO: shutdown the engine
        engine.shutdown(wait=False)
        self.content_frame.refresh_result_pannel()

    def progressbar_start(self):
        self.foot_frame.progressbar_start()

    def progressbar_stop(self):
        self.foot_frame.progressbar_stop()