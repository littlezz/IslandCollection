from tkinter import *
from tkinter import ttk
from .widgets import UrlSelectColumnFrame
__author__ = 'zz'

root = Tk()
root.title('Island Collections')

main_frame = ttk.Frame(root)
main_frame.grid(column=0, row=0)
for i in range(10):
    u = UrlSelectColumnFrame(main_frame)
    u.grid(column=0, row=i)

root.mainloop()