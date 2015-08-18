from .. import widgets
from .. import layouts
from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk
from core.compat import IS_WINDOWS
__author__ = 'zz'




class RowFrame(ttk.Frame):
    def __init__(self, master, **kwargs):
        image_url = kwargs.pop('image_url', None)
        image_fp = kwargs.pop('image_fp', None)
        text = kwargs.pop('text', '')
        link = kwargs.pop('link', '')
        super().__init__(master, **kwargs)


        self.image_frame = widgets.ImageFrame(self, image_url=image_url, image_fp=image_fp)

        self.link_label = widgets.HyperLabel(self, text=link, link=link, cursor='hand2', foreground='blue')
        self.text_label = ttk.Label(self, text=text)

        self.image_frame.grid(column=0, row=0, rowspan=2)
        self.link_label.grid(column=1, row=0, sticky='NW')
        self.text_label.grid(column=1, row=1, sticky='NW')



class FootFrame(widgets.BaseFrame):
    def _init(self):
        self.button = widgets.Button(self, text='Back', help_text='back')
        self.button.grid(column=0, row=0)

    def set_button_command(self, command):
        self.button.configure(command=command)


class SideFrame(widgets.BaseFrame):
    def _init(self):
        self.cb = widgets.ExtraDataComboBox(self,
                                            values_pair=(('has image', 'images'), ('content contain', 'text__in')),
                                            help_text='filter type')
        self.entry = widgets.Entry(self, help_text='filter args')
        self.submit = widgets.Button(self, text='filter', command=self.submit_filter)

        self.cb.grid(column=0, row=0)
        self.entry.grid(column=1, row=0)
        self.submit.grid(column=2, row=0)

    def submit_filter(self):
        filter_type = self.cb.get()
        args = self.entry.get()
        self.master.do_filter(filter_type=filter_type, args=args)


class ContentFrame(widgets.BaseFrame):
    def __init__(self, *args, results=None, **kwargs):
        self.results = results
        super().__init__(*args, **kwargs)

    def _init(self):

        # scrollable content
        self.canvas = tk.Canvas(self, height=400, width=400)
        self.frame = ttk.Frame(self.canvas)
        self.vbs = ttk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vbs.set)
        self.vbs.pack(side='right', fill='y')
        self.canvas.pack(side='left', fill='both', expand=True)
        self.canvas.create_window((4, 4), window=self.frame, anchor='nw', tag='self.frame')
        self.frame.bind('<Configure>', self.on_frame_configure)
        self.canvas.bind_all('<MouseWheel>', self._on_mousewheel)


        self.rows = 0

        self.show_results(self.results)

    def show_results(self, results):
        """
        generate the results
        """
        self.test()

    def on_frame_configure(self, e):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mousewheel(self, e):
        if IS_WINDOWS:
            self.canvas.yview_scroll(-int(e.delta/120), 'units')
        else:
            self.canvas.yview_scroll(-e.delta, 'units')

    def test(self):
        for i in range(5):
            im = Image.open('gui/images_test/1t.jpg')
            if i%2==0:
                r = RowFrame(self.frame, image_fp=im, text='the'+str(i), link='http://www.baidu.com')
            else:
                r = RowFrame(self.frame,image_fp=im, text='the'+str(i), link='http://www.baidu.com')
            r.grid(column=0, row=self.rows, sticky='NEWS')
            self.rows += 1

    def do_filter(self, filter_type, args):
        results = self.results.filter(**{filter_type: args})

        for child in self.frame.children:
            child.destory()

        # TODO: inject result to content
        # self.show_results(results)


class MainFrame(layouts.BaseMainFrameLayout):
    def _init(self):
        self.content_frame = ContentFrame(self)
        self.side_frame = SideFrame(self)
        self.foot_frame = FootFrame(self)


    def do_filter(self, filter_type, args=None):
        self.content_frame.do_filter(filter_type=filter_type, args=args)