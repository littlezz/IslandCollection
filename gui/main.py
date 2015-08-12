from tkinter import *
from tkinter import ttk

from gui.second.frames import MainFrame

__author__ = 'zz'


def next_frame(master):
    master.grid_forget()


root = Tk()
root.title('Island Collections')
root.minsize(width=666, height=666)

mainframe = MainFrame(root)
mainframe.grid(column=0, row=0, sticky='NWSE')

# ttk.Button(text='next', command=lambda : next_frame(mainframe)).grid(column=1, row=1)

root.mainloop()