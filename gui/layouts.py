from .widgets import BaseFrame
__author__ = 'zz'


dummy = object()


class FrameStack:
    def __init__(self, root, frame_list=None, now=None):
        self._root = root
        self._frames = list(frame_list) if frame_list else []
        self._now = now


    def previous_frame(self, pass_data):
        """
        change to previous frame
        :return:
        """
        now = self._now
        index = self._frames.index(now)
        to = self._frames[index-1]
        self.change_frame(now, to, pass_data)

    def next_frame(self, pass_data):
        now = self._now
        index = self._frames.index(now)
        to = self._frames[index+1]
        self.change_frame(now, to, pass_data)

    def change_frame(self, now, to, pass_data):
        now.grid_forget()
        to.grid(**to.get_grid_kwargs())
        self._now = to
        to.on_show(pass_data)
        # update frame
        self._root.update_idletasks()

    def add_frame(self, frame):
        self._frames.append(frame)

    def show(self):
        """
        at the beginning, show the "now" frame
        :return:
        """
        if self._now is None:
            self._now = self._frames[0]

        if not self._now.grid_info():
            self._now.grid(**self._now.get_grid_kwargs())


class BaseMainFrameLayout(BaseFrame):

    must_frames = ('side_frame', 'content_frame', 'foot_frame')
    side_frame = dummy
    content_frame = dummy
    foot_frame = dummy

    def __init__(self, master=None, **kwargs):
        self.top_stack = kwargs.pop('top_stack')

        super().__init__(master, **kwargs)

        self.top_stack.add_frame(self)

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

    def on_show(self, pass_data):
        """
        :kwargs data from last frame on_change method
        hook for do something when this frame is show
        """
        pass

    def on_change(self):
        """
        hook for do something when this frame is hide/change
        :return a dict contain data that pass to next/previous frame on_show method
        """
        pass

    def next_frame(self):
        pass_data = self.on_change()
        self.top_stack.next_frame(pass_data)

    def previous_frame(self):
        pass_data = self.on_change()
        self.top_stack.previous_frame(pass_data)

    def get_grid_kwargs(self):
        return {
            'column': 0,
            'row': 0,
            'sticky': 'NWSE',
        }