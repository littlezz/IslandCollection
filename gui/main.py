import tkinter
from gui import first, second
from gui import widgets
from gui.layouts import FrameStack

__author__ = 'zz'





root = widgets.RootTk()
root.title('Island Collections')
root.minsize(width=666, height=666)

fs = FrameStack(root=root)

f1 = first.MainFrame(root, top_stack=fs)
f2 = second.MainFrame(root, top_stack=fs)

fs.show()
# # todo:rewrite with engine
# fs = FrameStack(root=root, frame_list=[f1, f2], now=f1)

# f1.foot_frame.button.configure(command=fs.next_frame)
# f2.foot_frame.button.configure(command=fs.previous_frame)


# root.mainloop()