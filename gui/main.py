import tkinter
from gui import first, second
from gui import widgets
from gui.layouts import FrameStack

__author__ = 'zz'





root = widgets.RootTk()
root.title('Island Collections')
# root.minsize(width=666, height=666)
root.geometry("900x640")

fs = FrameStack(root=root)

f1 = first.MainFrame(root, top_stack=fs)
f2 = second.MainFrame(root, top_stack=fs)

fs.show()
