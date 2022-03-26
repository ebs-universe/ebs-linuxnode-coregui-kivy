

from ebs.linuxnode.core.basenode import BaseIoTNode

from .background import OverlayWindowGuiMixin
from .text import FontsGuiMixin
from .log import LoggingGuiMixin
from .busy import BusySpinnerGuiMixin
from .nodeid import NodeIDGuiMixin


class BaseIoTNodeGui(NodeIDGuiMixin,
                     BusySpinnerGuiMixin,
                     LoggingGuiMixin,
                     FontsGuiMixin,
                     OverlayWindowGuiMixin):

    def __init__(self, *args, **kwargs):
        self._application = kwargs.pop('application')
        self._gui_root = None
        super(BaseIoTNodeGui, self).__init__(*args, **kwargs)

    @staticmethod
    def _gui_disable_multitouch_emulation():
        from kivy.config import Config
        Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

    def gui_setup(self):
        self._gui_disable_multitouch_emulation()
        super(BaseIoTNodeGui, self).gui_setup()
        return self.gui_root
