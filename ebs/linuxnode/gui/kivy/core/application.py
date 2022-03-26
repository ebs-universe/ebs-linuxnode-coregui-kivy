

from kivy.app import App
from twisted.internet import reactor

from ebs.linuxnode.gui.kivy.core.basenode import BaseIoTNodeGui


class BaseIOTNodeApplication(App):
    def __init__(self, config, *args, **kwargs):
        self._config = config
        self._debug = kwargs.pop('debug', False)
        super(BaseIOTNodeApplication, self).__init__(*args, **kwargs)
        self._node = None

    def build(self):
        print("Constructing Node")
        self._node = BaseIoTNodeGui(reactor=reactor, application=self)
        print("Installing Node Resources")
        self._node.install()
        print("Building GUI for node {0}".format(self._node))
        return self._node.gui_setup()

    def on_start(self):
        self._node.start()

    def on_stop(self):
        self._node.stop()

    def on_pause(self):
        pass
