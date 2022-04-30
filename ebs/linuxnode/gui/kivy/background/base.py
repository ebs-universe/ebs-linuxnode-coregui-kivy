

class BackgroundProviderBase(object):
    is_visual = True

    def __init__(self, actual):
        self._actual = actual
        self._widget = None

    @property
    def actual(self):
        if hasattr(self._actual, 'actual'):
            return self._actual.actual
        else:
            return self._actual

    def check_support(self, target):
        # Check if the provider supports the target and
        # if the target exists.
        raise NotImplementedError

    def play(self, target, duration=None, callback=None, **kwargs):
        # Create a Widgetized Background and return it.
        # It will be attached later.
        raise NotImplementedError

    def stop(self):
        # Stop and unload the Widgetized Background.
        # The widget has already been detached.
        raise NotImplementedError

    def pause(self):
        # Pause the Widgetized Background.
        # It has already been detached.
        raise NotImplementedError

    def resume(self):
        # Resume the Widgetized Background.
        # It will be attached later.
        raise NotImplementedError
