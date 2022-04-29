

from itertools import cycle

from .manager import BackgroundGuiMixin
from .manager import BackgroundSpec


class BackgroundSequenceMixin(BackgroundGuiMixin):
    def __init__(self, *args, **kwargs):
        super(BackgroundSequenceMixin, self).__init__(*args, **kwargs)
        self._bg_sequence = cycle([])

    @property
    def gui_bg_sequence(self):
        return self._bg_sequence

    @gui_bg_sequence.setter
    def gui_bg_sequence(self, value):
        self._bg_sequence = cycle(value)
        self.gui_bg_step()

    def gui_bg_step(self, *_):
        target = next(self.gui_bg_sequence)
        bgcolor, callback, duration = None, None, None
        if isinstance(target, BackgroundSpec):
            target, bgcolor, callback, duration = target

        if not bgcolor:
            bgcolor = self.config.image_bgcolor

        if callback:
            self.log.warn("BG Sequence recieved an item with a callback. "
                          "This is not supported and is ignored. {}".format(target))

        callback = self.gui_bg_step
        spec = BackgroundSpec(target, bgcolor, callback, duration)
        self.log.debug("BG Sequence Step : {}".format(spec))
        self.gui_bg = spec
