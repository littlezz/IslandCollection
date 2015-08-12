from .. import widgets
from .. import layouts
from tkinter import ttk
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
            self.image_label.grid(column=0, row=0)
            self.image_label.image=image

        # todo: clickable
        self.link_label = widgets.HyperLabel(self, text=link, link=link, cursor='hand2', foreground='blue')
        self.text_label = widgets.HyperLabel(self, text=text, link=link)

        self.link_label.grid(column=1, row=0)
        self.text_label.grid(column=1, row=1)

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
        self.rows = 0
        self.test()

    def test(self):
        for i in range(5):

            r = RowFrame(self, text='the'+str(i), link='http://www.baidu.com')
            r.grid(column=0, row=self.rows)
            self.rows += 1



class MainFrame(layouts.BaseMainFrameLayout):
    def _init(self):
        self.content_frame = ContentFrame(self)
        self.side_frame = SideFrame(self)
        self.foot_frame = FootFrame(self)
