

from .base import BackgroundProviderBase


class StructuredBackgroundProvider(BackgroundProviderBase):
    def check_support(self, target):
        if not isinstance(target, str):
            return False
        if not target.startswith('structured:'):
            return False
        if not hasattr(self.actual, target.split(':')[1]):
            return False
        return True

    def play(self, target, **kwargs):
        _target = getattr(self.actual, target.split(':')[1])
        if callable(_target):
            self._widget = _target(**kwargs)
        else:
            self._widget = _target
        return self._widget

    def stop(self):
        if hasattr(self._widget, 'stop'):
            self._widget.stop()
        self._widget = None

    def pause(self):
        if hasattr(self._widget, 'pause'):
            self._widget.pause()

    def resume(self):
        if hasattr(self._widget, 'retrigger'):
            self._widget.retrigger()
