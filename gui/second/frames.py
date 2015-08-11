from .. import widgets
from tkinter import ttk
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
            self.image_label = ttk.Label(self, image=image)
            self.image_label.grid(column=0, row=0)

        # todo: clickable
        self.link_label = ttk.Label(self, text=link)
        self.text_label = ttk.Label(self, text=text)

        self.link_label.grid(column=1, row=0)
        self.text_label.grid(column=1, row=1)


class FootFrame(widgets.BaseFrame):
    def _init(self):
        self.button = widgets.Button(self, text='Back', help_text='back')
        self.button.grid(column=0, row=0)

    def set_button_command(self, command):
        self.button.configure(command=command)
