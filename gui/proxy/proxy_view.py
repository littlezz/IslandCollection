__author__ = 'zz'

import json
from .. import widgets
from core import proxy
from tkinter import ttk

class LabelEntry(ttk.Frame):
    _entry_class = widgets.Entry

    def __init__(self, master, *args, **kwargs):
        label_text = kwargs.pop('label_text')
        super().__init__(master)
        self.label = ttk.Label(self, text=label_text)
        self.entry = self._entry_class(self, *args, **kwargs)

        self.label.grid(column=0, row=0)
        self.entry.grid(column=1, row=0)

        self.get = self.entry.get
        self.set = self.entry.set


class LabelNumberEntry(LabelEntry):
    _entry_class = widgets.NumberEntry





class ProxyDataView(widgets.BaseFrame):
    def _init(self):

        self.ip_entry = LabelEntry(self, label_text='ip address')
        self.port_entry = LabelEntry(self, label_text='port', help_text='port')
        self.ok_button = widgets.Button(self, text='set!', help_text='set and save', command=self._on_ok)
        self.clear_button = widgets.Button(self, text='clear!', command=self._on_clear)

        self.ip_entry.pack()
        self.port_entry.pack()
        self.ok_button.pack()
        self.clear_button.pack()


        self.show_data()

    def _on_clear(self):
        self.ip_entry.set('')
        self.port_entry.set('')
        self.ok_button.invoke()


    def _on_ok(self):
        addr = self.ip_entry.get()
        port = self.port_entry.get()
        if port:
            port = int(port)

        proxy.set_proxy(addr, port)

        data = {
            'address': addr,
            'port': port,
        }

        with open('proxy.json', 'w', encoding='utf8') as f:
            json.dump(obj=data, fp=f)


    def show_data(self):
        try:
            with open('proxy.json', encoding='utf8') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}

        self.ip_entry.set(data.get('address', ''))
        self.port_entry.set(data.get('port', ''))









