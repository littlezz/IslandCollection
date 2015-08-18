from .widgets import BaseFrame
__author__ = 'zz'


dummy = object()


class BaseMainFrameLayout(BaseFrame):

    must_frames = ('side_frame', 'content_frame', 'foot_frame')
    side_frame = dummy
    content_frame = dummy
    foot_frame = dummy

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(padding='5 5 5 5')
        self.layout()


    def assert_dummy(self):
        for name in self.must_frames:
            assert getattr(self, name) is not dummy, 'must set {} in {}'.format(name, self.__class__)

    def layout(self):
        self.assert_dummy()

        self.content_frame.configure(padding='5 5 5 5')
        self.content_frame.grid(column=0, row=0)
        self.side_frame.grid(column=1, row=0, sticky='NW')
        self.foot_frame.grid(column=0, row=1)

    def on_show(self, **kwargs):
        pass
