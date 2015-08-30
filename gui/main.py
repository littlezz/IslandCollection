from tkinter import ttk
from gui import first, second, bookmark
from gui import widgets
from gui.layouts import FrameStack
from core.database import connect_to_db
import os
from core import settings

__author__ = 'zz'


# prepare
connect_to_db()
try:
    os.mkdir(settings.IMAGE_CACHE_PATH)
except FileExistsError:
    pass


root = widgets.RootTk()
root.title('Island Collections')
root.geometry("900x650")


notebook = ttk.Notebook(root, padding=2)

search_frame = ttk.Frame(notebook)
book_frame = bookmark.MainFrame(notebook)
notebook.add(search_frame, text='主程序')
notebook.add(book_frame, text='收藏夹')

notebook.pack()

fs = FrameStack(root=search_frame)

f1 = first.MainFrame(search_frame, top_stack=fs)
f2 = second.MainFrame(search_frame, top_stack=fs)

fs.show()
