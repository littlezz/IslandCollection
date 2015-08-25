from PIL import Image, ImageTk
import tkinter
from tkinter import ttk
from gui.second.frames import RowFrame, ResultInfo
__author__ = 'zz'

class BaseTestFrame(ttk.Frame):
    _master = None
    def __init__(self, master=None, **kwargs ):
        if master is None:
            master = self._master
        super().__init__(master, **kwargs)

        self._time_set = False
        self.pack()
        self.test()
        if not self._time_set:
            self.set_destroy_time(1500)

    def set_destroy_time(self, ms):
        self._time_set = True
        self.after(ms, self.destroy)

    def test(self):
        raise NotImplementedError

    def destroy(self):
        self._master.event_generate("<<next>>")
        super().destroy()




root  = tkinter.Tk()
BaseTestFrame._master = root



########### Test ##################


# test normal image show
class Test1(BaseTestFrame):
    def test(self):
        im = Image.open('gui/images_test/1.png')
        im = ImageTk.PhotoImage(im)

        image_label = ttk.Label(self, image=im)
        image_label.ima = im

        image_label.pack()


# test Row in second/frames
class Test2(BaseTestFrame):
    def test(self):
        from gui.second.frames import ResultInfo, RowFrame
        r = ResultInfo(text='test', link='http://example.com', response_num=20)
        RowFrame(self, **r.as_dict()).pack()


class Test3(BaseTestFrame):
    def test(self):
        from gui.second.frames import ResultInfo, RowFrame
        im = Image.open('gui/images_test/1.png')
        r = ResultInfo(text='test', link='http://example.com', response_num=20, image_fp=im)
        RowFrame(self, **r.as_dict()).pack()


class Test4(BaseTestFrame):
    def test(self):
        from gui.second.frames import ResultInfo, RowFrame

        r = ResultInfo(text='test', link='http://example.com', response_num=20, image_url='https://www.baidu.com/img/bd_logo1.png')
        RowFrame(self, **r.as_dict()).pack()
        self.set_destroy_time(3500)


# test for processbar

class Test5(BaseTestFrame):
    def test(self):
        pb = ttk.Progressbar(self, orient=tkinter.HORIZONTAL, mode='determinate')
        pb.pack()
        pb.start()
        self.set_destroy_time(4000)


############ main run test function #########

def run_test():
    BaseTestFrame._master = root
    pipe = (item[1] for item in globals().items() if item[0].startswith('Test'))
    def next_pipe(*args):
        print("next")
        try:
            t = next(pipe)
            t()
        except StopIteration:
            print('finish!')
            root.quit()

    root.bind("<<next>>", next_pipe)
    root.after(0, next_pipe)
    root.mainloop()

if __name__ == '__main__':
    run_test()

