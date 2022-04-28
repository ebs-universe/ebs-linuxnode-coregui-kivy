

import os
import shutil
import appdirs
from kivy.uix.boxlayout import BoxLayout

from ebs.linuxnode.core.config import ElementSpec, ItemSpec
from ebs.linuxnode.gui.kivy.core.basemixin import BaseGuiMixin

from .image import ImageBackgroundProvider
from .color import ColorBackgroundProvider


class BackgroundGuiMixin(BaseGuiMixin):
    def __init__(self, *args, **kwargs):
        self._bg_providers = []
        self._bg_container = None
        self._bg = None
        self._bg_current = None
        self._bg_current_provider = None
        super(BackgroundGuiMixin, self).__init__(*args, **kwargs)

    def install_background_provider(self, provider):
        self.log.info("Installing BG Provider {}".format(provider))
        self._bg_providers.append(provider)

    def install(self):
        super(BackgroundGuiMixin, self).install()

        _path = os.path.abspath(os.path.dirname(__file__))
        fallback_default = os.path.join(_path, 'images/background.png')
        fallback = os.path.join(appdirs.user_config_dir(self.config.appname), 'background.png')
        if not os.path.exists(fallback):
            shutil.copy(fallback_default, fallback)

        _elements = {
            'image_bgcolor': ElementSpec('display', 'image_bgcolor', ItemSpec('kivy_color', fallback='auto')),
            'background': ElementSpec('display', 'background', ItemSpec(str, read_only=False, fallback=fallback)),
        }
        for name, spec in _elements.items():
            self.config.register_element(name, spec)

        self.install_background_provider(ImageBackgroundProvider(self))
        self.install_background_provider(ColorBackgroundProvider(self))

    def background_set(self, target):
        if not target:
            target = None

        if self.bg_is_structured(fpath):
            if not hasattr(self, fpath.split(self._bg_separator)[1]):
                fpath = None
        else:
            if not os.path.exists(fpath):
                fpath = None

        if self.config.background != fpath:
            old_bg = os.path.basename(urlparse(self.config.background).path)
            if self.bg_is_file(old_bg) and self.resource_manager.has(old_bg):
                self.resource_manager.remove(old_bg)
            self.config.background = fpath

        self.gui_bg_update()

    @property
    def gui_bg_container(self):
        if self._bg_container is None:
            self._bg_container = BoxLayout()
            self.gui_main_content.add_widget(self._bg_container)
        return self._bg_container

    def gui_bg_clear(self):
        if self._bg and self._bg.parent:
            self.gui_bg_container.remove_widget(self._bg)
        self._bg = None
        if self._bg_current_provider:
            self._bg_current_provider.stop()

    @property
    def gui_bg(self):
        return self._bg_current

    @gui_bg.setter
    def gui_bg(self, value):
        self.log.info("Setting background to {value}", value=value)

        provider: BackgroundProviderBase
        provider = None
        for lprovider in self._bg_providers:
            if lprovider.check_support(value):
                self.log.debug("Using provider {} to set bg to {}."
                               "".format(lprovider.__class__, value))
                provider = lprovider
                break

        if not provider:
            self.log.warn("Providernot found for background {}".format(value))
            value = self.config.background

        if value == self._bg_current:
            return

        self.gui_bg_clear()

        self._bg_current = value
        self._bg_current_provider = provider
        self._bg = self._bg_current_provider.play(value, bgcolor=self.config.image_bgcolor)
        self.gui_bg_container.add_widget(self._bg)

    def gui_bg_update(self):
        self.gui_bg = self.config.background

    def gui_bg_pause(self):
        self.log.debug("Pausing Background")
        self.gui_main_content.remove_widget(self._bg_container)
        if self._bg_current_provider:
            self._bg_current_provider.pause()

    def gui_bg_resume(self):
        self.log.debug("Resuming Background")
        if self._bg_current_provider:
            self._bg_current_provider.resume()
        if not self._bg_container.parent:
            self.gui_main_content.add_widget(self._bg_container, len(self.gui_main_content.children))

    def stop(self):
        if self._bg_current_provider:
            self._bg_current_provider.stop()
        super(BackgroundGuiMixin, self).stop()

    def gui_setup(self):
        super(BackgroundGuiMixin, self).gui_setup()
        self.gui_bg = self.config.background
