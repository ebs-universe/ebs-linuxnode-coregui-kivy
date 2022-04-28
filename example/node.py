

from twisted.internet import reactor
from kivy_garden.ebs.clocks.digital import SimpleDigitalClock
from ebs.linuxnode.gui.kivy.core.basenode import BaseIoTNodeGui


class ExampleNode(BaseIoTNodeGui):
    def _set_bg(self, target):
        self.gui_bg = target

    @property
    def clock(self):
        return SimpleDigitalClock()

    def start(self):
        reactor.callLater(10, self._set_bg, '1.0:0.5:0.5:1.0')
        reactor.callLater(20, self._set_bg, 'image.jpg')
        reactor.callLater(30, self._set_bg, '0.5:1.0:0.5:1.0')
        reactor.callLater(40, self._set_bg, None)
        # Install kivy_garden.ebs.clocks
        # reactor.callLater(50, self._set_bg, 'structured:clock')
        super(ExampleNode, self).start()
