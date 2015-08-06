from tkinter import *
from tkinter import ttk
from gui.url_set_notebook import UrlSelectColumnFrame
from .url_set_notebook import NoteFrame

__author__ = 'zz'




root = Tk()
root.title('Island Collections')
root.minsize(width=666, height=666)
mainframe = NoteFrame(root)
mainframe.grid(column=0, row=0)

root.mainloop()