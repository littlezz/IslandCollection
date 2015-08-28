from tkinter import ttk
from .. import widgets
from PIL import Image
from core.database import Bookmark
import os.path
import requests
from core import analyzer
from core import settings

__author__ = 'zz'


class BookAddFrame(widgets.BaseFrame):
    save_to_prefix = settings.IMAGE_CACHE_PATH

    def _init(self):
        self.url_label = ttk.Label(self, text='Url')
        self.url_entry = widgets.Entry(self)
        self.add_button = widgets.Button(self, text='Add', command=self.add_bookmark)

        self.url_label.grid(column=0, row=0)
        self.url_entry.grid(column=1, row=0)
        self.add_button.grid(column=2, row=0)


    def add_bookmark(self):
        url = self.url_entry.get()
        url = analyzer.init_start_url(url)
        req = requests.get(url)
        result = analyzer.get_thread_info(url, req)

        kwargs = result.as_dict()
        query = kwargs.copy()

        if result.has_image:
            image_name = result.image_url.rsplit('/', 1)[-1]
            path = os.path.join(self.save_to_prefix, image_name)
            kwargs.update(image_save_to=path)
            query.update(image_path=path)

        query.pop('image_url', '')
        query.pop('image_fp', '')
        Bookmark.create(**query)

        self.master.add_bookmark(**kwargs)


class BookmarkRow(widgets.BaseRowFrame):
    _text_width = 65
    _text_wraplength = 500

    def __init__(self, *args, **kwargs):
        self.database_id = kwargs.pop('id', None)
        super().__init__(*args, **kwargs)

    def create_widgets(self):
        super().create_widgets()
        self.delete_button = widgets.Button(self, text='-', width=2, command=self.delete)
        self.delete_button.grid(column=3, row=0, sticky='nw')

    def delete(self):
        Bookmark.delete_by_id(self.database_id)
        self.destroy()


class BookmarkView(widgets.ScrollbarCanvasMixin, widgets.BaseFrame):
    canvas_height = 550
    canvas_width = 850

    def _init(self):
        super()._init()
        self.rows = 0
        self.show_bookmarks()

    def show_bookmarks(self):
        bs = Bookmark.get_all()
        if bs.exists():
            for row_info in bs:
                image_path = row_info.pop('image_path', '')
                if image_path and os.path.exists(image_path):
                    image_fp = Image.open(image_path)
                    row_info.update(image_fp=image_fp)

                self.add_one_row(**row_info)


    def add_one_row(self, **kwargs):
        r = BookmarkRow(self.frame, **kwargs)
        r.grid(column=0, row=self.rows)
        self.rows += 1



class MainFrame(widgets.BaseFrame):
    def _init(self):
        self.add_frame = BookAddFrame(self)
        self.book_view = BookmarkView(self)

        self.add_frame.grid(column=0, row=0)
        self.book_view.grid(column=0, row=1)

        self.book_view.bind_class_mousewheel('BookmarkRow')

    def add_bookmark(self, **kwargs):
        self.book_view.add_one_row(**kwargs)


