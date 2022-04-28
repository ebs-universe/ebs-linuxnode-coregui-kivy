

import os
from kivy_garden.ebs.core.image import BleedImage

from .base import BackgroundProviderBase


class ImageBackgroundProvider(BackgroundProviderBase):
    def check_support(self, target):
        if not isinstance(target, str):
            return False
        if not os.path.exists(target):
            return False
        _extentions = ('.png', '.jpg', '.bmp', '.gif', '.jpeg')
        if os.path.splitext(target)[1] not in _extentions:
            return False
        return True

    def play(self, target, **kwargs):
        self._widget = BleedImage(
            source=target,
            allow_stretch=True,
            keep_ratio=True,
            **kwargs
        )
        return self._widget

    def stop(self):
        self._widget = None

    def pause(self):
        pass

    def resume(self):
        pass