from tkinter import ttk
import tkinter as tk
from .. import widgets

__author__ = 'zz'

class BookAddFrame(widgets.BaseFrame):
    def _init(self):
        self.url_label = ttk.Label(self, text='Url')
        self.url_entry = widgets.Entry(self)
        self.add_button = widgets.Button(self, text='Add', command=self.add_bookmark)

        self.url_label.grid(column=0, row=0)
        self.url_entry.grid(column=1, row=0)
        self.add_button.grid(column=2, row=0)


    def add_bookmark(self):
        pass

class BookmarkView(widgets.ScrollbarCanvasMixin, widgets.BaseFrame):
    canvas_height = 500
    canvas_width = 800

    def _init(self):
        pass