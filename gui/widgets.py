from tkinter import ttk
import tkinter
import webbrowser
import requests
from io import BytesIO
from PIL import Image, ImageTk
from core.compat import IS_WINDOWS
from .threadpool import thread_pool as _thread_pool
from urllib import parse
__author__ = 'zz'




class VarGetSetMixin:
    def get(self):
        return self.var.get()

    def set(self, value):
       self.var.set(value=value)




class StringVarMixin(VarGetSetMixin):
    def __init__(self, *args, **kwargs):
        value = kwargs.pop('value', None)
        self.var = tkinter.StringVar(value=value)
        kwargs.update(textvariable=self.var)
        super().__init__(*args, **kwargs)


class HelpTextMixin:
    def __init__(self, *args, **kwargs):
        self.help_text = kwargs.pop('help_text','')
        super().__init__(*args, **kwargs)


class HyperMixin:
    def __init__(self, *args, **kwargs):
        self._link = kwargs.pop('link', '')
        super().__init__(*args, **kwargs)
        self.bind('<1>', self._click)

    def _click(self, event):
        webbrowser.open(self._get_url())

    def _get_url(self):
        return self._link





class CheckButton(HelpTextMixin, VarGetSetMixin, ttk.Checkbutton):
    def __init__(self, master, value=1, **kwargs):
        self.var = tkinter.IntVar(value=value)
        kwargs.update(variable=self.var)
        super().__init__(master, **kwargs)


class Button(HelpTextMixin, ttk.Button):
    pass


class Entry(HelpTextMixin, StringVarMixin, ttk.Entry):
    pass


class UrlEntry(Entry):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.var.trace('w', self._unquote_text)

    def _unquote_text(self, *args):
        self.var.set(parse.unquote(self.var.get()))



class NumberEntry(HelpTextMixin, VarGetSetMixin, ttk.Entry):
    def __init__(self, master, value=None, **kwargs):
        super().__init__(master, **kwargs)
        self.var = tkinter.IntVar(value=value)
        vcmd = (self.register(self.validating), '%S')

        cf = dict()
        cf.update(textvariable=self.var)
        cf.update(validatecommand=vcmd)
        cf.update(validate='key')
        self.configure(**cf)


    def validating(self, text):
        allow = '0123456789'
        if all(c in allow for c in text):
            return True
        return False


class InfoLabel(HelpTextMixin, StringVarMixin, ttk.Label):
    pass


class HyperLabel(HyperMixin, ttk.Label):
    pass


class ImageFrame(ttk.Frame):
    height = 192
    width = 192
    def __init__(self, *args, **kwargs):
        self.image_url = kwargs.pop('image_url', None)
        self.image_fp = kwargs.pop('image_fp', None)
        self.save_to = kwargs.pop('save_to', None)
        kwargs.update({
            'height':self.height,
            'width': self.width
        })
        super().__init__(*args, **kwargs)
        self.grid_propagate(0)

        if self.image_url:
            self.label = ttk.Label(self, text='downloading...')
            _thread_pool.submit(self.download_image)

        elif self.image_fp:
            im = self.image_fp
            im.thumbnail((self.width, self.height))
            im = ImageTk.PhotoImage(im)
            self.label = ttk.Label(self, image=im)
            self.label.image = im
        else:
            self.label = ttk.Label(self, text='No Image')

        self.label.grid(column=0, row=0, sticky='W')

    def download_image(self):
        data = requests.get(self.image_url).content
        fp = BytesIO(data)
        im = Image.open(fp)

        im.thumbnail((self.width, self.height))

        if self.save_to:
            im.save(self.save_to)

        im = ImageTk.PhotoImage(im)
        self.label.image = im
        self.label.configure(image=im)


class ExtraDataComboBox(HelpTextMixin, ttk.Combobox):
    def __init__(self, *args, **kwargs):
        values_pair = kwargs.pop('values_pair', [])
        values = []
        self._maps = dict()
        for pair in values_pair:
            value, extra = pair
            self._maps.update({value:extra})
            values.append(value)

        kwargs.update(values=values)
        super().__init__(*args, **kwargs)

    def get(self):
        value = super().get()
        return self._maps[value]


def retags(w, tag):
    w.bindtags((tag, ) + w.bindtags())


class BaseRowFrame(ttk.Frame):
    _text_width = 44
    _text_wraplength = 345

    def __init__(self, master, **kwargs):
        self.image_url = kwargs.pop('image_url', None)
        self.image_fp = kwargs.pop('image_fp', None)
        self.text = kwargs.pop('text', '')
        self.link = kwargs.pop('link', '')
        self.response_num = int(kwargs.pop('response_num', 0))
        self.image_save_to = kwargs.pop('image_save_to', None)

        kwargs['class_'] = self.__class__.__name__
        super().__init__(master, **kwargs)

        self.create_widgets()
        for w in self.winfo_children():
            retags(w, kwargs['class_'])

    def create_widgets(self):

        self.image_frame = ImageFrame(self, image_url=self.image_url, image_fp=self.image_fp, save_to=self.image_save_to)

        self.link_label = HyperLabel(self, text=self.link, link=self.link, cursor='hand2', foreground='blue')
        self.text_label = ttk.Label(self, text=self.text, width=self._text_width, wraplength=self._text_wraplength)
        self.response_num_label = ttk.Label(self, text='replies: ' + str(self.response_num))

        self.image_frame.grid(column=0, row=0, rowspan=2)
        self.link_label.grid(column=1, row=0, sticky='N')
        self.response_num_label.grid(column=2, row=0, sticky='NW')
        self.text_label.grid(column=1, row=1, sticky='NW', columnspan=2)

        self.separator = ttk.Separator(self, orient=tkinter.HORIZONTAL)
        self.separator.grid(column=0, row=2, columnspan=3, sticky='we', pady=7, padx=25)

    @property
    def has_image(self):
        return True if self.image_url or self.image_fp else False





class BaseFrame(ttk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self._init()

    def _init(self):
        raise NotImplementedError


class RootTk(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        _thread_pool.shutdown(wait=False)
        self.destroy()


class ScrollbarCanvasMixin(BaseFrame):
    canvas_height = 570
    canvas_width = 550

    def _init(self):

        self.canvas = tkinter.Canvas(self, height=self.canvas_height, width=self.canvas_width)
        self.frame = ttk.Frame(self.canvas)
        self.vbs = ttk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vbs.set)
        self.vbs.pack(side='right', fill='y')
        self.canvas.pack(side='left', fill='both', expand=True)
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw', tag='self.frame')
        self.frame.bind('<Configure>', self.on_frame_configure)
        # self.canvas.bind_all('<MouseWheel>', self._on_mousewheel)
        self.canvas.bind('<MouseWheel>', self._on_mousewheel)
        self.frame.bind('<MouseWheel>', self._on_mousewheel)

    def on_frame_configure(self, e):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mousewheel(self, e):
        if IS_WINDOWS:
            self.canvas.yview_scroll(-int(e.delta/120), 'units')
        else:
            self.canvas.yview_scroll(-e.delta, 'units')

    def bind_class_mousewheel(self, class_name):
        self.bind_class(class_name, '<MouseWheel>', self._on_mousewheel)