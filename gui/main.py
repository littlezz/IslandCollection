from tkinter import ttk
from gui import first, second
from gui import widgets
from gui.layouts import FrameStack
from core.database import connect_to_db

__author__ = 'zz'



connect_to_db()

root = widgets.RootTk()
root.title('Island Collections')
# root.minsize(width=666, height=666)
root.geometry("900x680")


notebook = ttk.Notebook(root, padding=2)

search_frame = ttk.Frame(notebook)
book_frame = ttk.Frame(notebook)
notebook.add(search_frame, text='主程序')
notebook.add(book_frame, text='收藏夹')

notebook.pack()
fs = FrameStack(root=search_frame)

f1 = first.MainFrame(search_frame, top_stack=fs)
f2 = second.MainFrame(search_frame, top_stack=fs)

fs.show()
