from .. import widgets
from .. import layouts
from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk
__author__ = 'zz'



class RowFrame(ttk.Frame):
    def __init__(self, master, **kwargs):
        image = kwargs.pop('image', None)
        text = kwargs.pop('text', '')
        link = kwargs.pop('link', '')
        size = kwargs.pop('size', (128, 128))
        super().__init__(master, **kwargs)

        if image:
            image.thumbnail(size)
            image = ImageTk.PhotoImage(image)
            self.image_label = ttk.Label(self, image=image)
            self.image_label.grid(column=0, row=0, rowspan=2)
            self.image_label.image=image

        # todo: clickable
        self.link_label = widgets.HyperLabel(self, text=link, link=link, cursor='hand2', foreground='blue')
        self.text_label = widgets.HyperLabel(self, text=text, link=link)

        self.link_label.grid(column=1, row=0, sticky='NW')
        self.text_label.grid(column=1, row=1, sticky='NW')


    def _get_url(self):
        return self.link_label['text']


class FootFrame(widgets.BaseFrame):
    def _init(self):
        self.button = widgets.Button(self, text='Back', help_text='back')
        self.button.grid(column=0, row=0)

    def set_button_command(self, command):
        self.button.configure(command=command)


class SideFrame(ttk.Frame):
    pass


class ContentFrame(widgets.BaseFrame):
    def _init(self):

        # scrollable content
        self.canvas = tk.Canvas(self, height=400, width=400)
        self.frame = ttk.Frame(self.canvas)
        self.vbs = ttk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vbs.set)
        self.vbs.pack(side='right', fill='y')
        self.canvas.pack(side='left', fill='both', expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor='nw', tag='self.frame')
        self.frame.bind('<Configure>', self.on_frame_configure)
        # root = self
        # self.canvas = tk.Canvas(root, borderwidth=0, background="#ffffff")
        # self.frame = ttk.Frame(self.canvas, background="#ffffff")
        # self.vsb = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        # self.canvas.configure(yscrollcommand=self.vsb.set)
        # self.vsb.pack(side="right", fill="y")
        # self.canvas.pack(side="left", fill="both", expand=True)
        # self.canvas.create_window((4,4), window=self.frame, anchor="nw",
        #                           tags="self.frame")
        # self.frame.bind("<Configure>", self.on_frame_configure)

        self.rows = 0
        self.test()

    def on_frame_configure(self, e):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def test(self):
        for i in range(5):
            im = Image.open('gui/images_test/1t.jpg')
            r = RowFrame(self.frame, image=im, text='the'+str(i), link='http://www.baidu.com')

            r.grid(column=0, row=self.rows, sticky='NEWS')
            self.rows += 1



class MainFrame(layouts.BaseMainFrameLayout):
    def _init(self):
        self.content_frame = ContentFrame(self)
        self.side_frame = SideFrame(self)
        self.foot_frame = FootFrame(self)
