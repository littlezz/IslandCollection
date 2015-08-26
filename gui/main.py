import tkinter
from gui import first, second
from gui import widgets
from gui.layouts import FrameStack
from core.database import connect_to_db

__author__ = 'zz'



connect_to_db()

root = widgets.RootTk()
root.title('Island Collections')
# root.minsize(width=666, height=666)
root.geometry("900x640")

fs = FrameStack(root=root)

f1 = first.MainFrame(root, top_stack=fs)
f2 = second.MainFrame(root, top_stack=fs)

fs.show()
