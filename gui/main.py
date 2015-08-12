import tkinter
from tkinter import ttk

from gui import first, second

__author__ = 'zz'


class FrameStack:
    def __init__(self, frame_list, now=None):
        self._frames = list(frame_list)
        self._now = now or self._frames[0]

    def previous_frame(self):
        """
        change to previous frame
        :return:
        """
        now = self._now
        index = self._frames.index(now)
        to = self._frames[index-1]
        self.change_frame(now, to)


    def next_frame(self):
        now = self._now
        index = self._frames.index(now)
        to = self._frames[index+1]
        self.change_frame(now, to)


    def change_frame(self, now, to):
        now.grid_forget()
        to.grid(**self._get_grid_kwargs())
        self._now = to

    def _get_grid_kwargs(self):
        return {
            'column': 0,
            'row': 0,
        }



def change_frame(self, to):
    self.grid_forget()
    to.grid(column=0, row=0)

root = tkinter.Tk()
root.title('Island Collections')
root.minsize(width=666, height=666)

f1 = first.MainFrame(root)
f2 = second.MainFrame(root)
f1.grid(column=0, row=0, sticky='NWSE')

fs = FrameStack(frame_list=[f1, f2], now=f1)

f1.foot_frame.button.configure(command=fs.next_frame)
f2.foot_frame.button.configure(command=fs.previous_frame)

# ttk.Button(text='next', command=lambda : next_frame(mainframe)).grid(column=1, row=1)

root.mainloop()