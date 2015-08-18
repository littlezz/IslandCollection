import tkinter
from gui import first, second
from gui import widgets

__author__ = 'zz'


class FrameStack:
    def __init__(self, root, frame_list, now=None):
        self._root = root
        self._frames = list(frame_list)
        self._now = now or self._frames[0]

        if not self._now.grid_info():
            self._now.grid(**self._get_grid_kwargs())

    def previous_frame(self, **kwargs):
        """
        change to previous frame
        :return:
        """
        now = self._now
        index = self._frames.index(now)
        to = self._frames[index-1]
        self.change_frame(now, to, **kwargs)


    def next_frame(self, **kwargs):
        now = self._now
        index = self._frames.index(now)
        to = self._frames[index+1]
        self.change_frame(now, to, **kwargs)


    def change_frame(self, now, to, **kwargs):
        now.grid_forget()
        to.grid(**self._get_grid_kwargs())
        self._now = to
        to.on_show(**kwargs)
        # update frame
        self._root.update()


    def _get_grid_kwargs(self):
        return {
            'column': 0,
            'row': 0,
            'sticky': 'NWSE',
        }



root = widgets.RootTk()
root.title('Island Collections')
root.minsize(width=666, height=666)

f1 = first.MainFrame(root)
f2 = second.MainFrame(root)

# todo:rewrite with engine
fs = FrameStack(root=root, frame_list=[f1, f2], now=f1)

f1.foot_frame.button.configure(command=fs.next_frame)
f2.foot_frame.button.configure(command=fs.previous_frame)


# root.mainloop()