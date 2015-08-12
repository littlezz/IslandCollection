from tkinter import *
from tkinter import ttk

from gui import first, second

__author__ = 'zz'


def change_frame(self, to):
    self.grid_forget()
    to.grid(column=0, row=0)

root = Tk()
root.title('Island Collections')
root.minsize(width=666, height=666)

f1 = first.MainFrame(root)
f2 = second.MainFrame(root)
f1.grid(column=0, row=0, sticky='NWSE')

f1.foot_frame.button.configure(command=lambda : change_frame(f1, f2))
f2.foot_frame.button.configure(command=lambda : change_frame(f2, f1))

# ttk.Button(text='next', command=lambda : next_frame(mainframe)).grid(column=1, row=1)

root.mainloop()