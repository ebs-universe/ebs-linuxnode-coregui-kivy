

import os
from kivy.core.window import Window
from ebs.linuxnode.core.config import ElementSpec, ItemSpec

from .manager import BackgroundGuiMixin


class OverlayWindowGuiMixin(BackgroundGuiMixin):
    # Overlay mode needs specific host support.
    # RPi :
    #   See DISPMANX layers and
    #   http://codedesigner.de/articles/omxplayer-kivy-overlay/index.html
    # Normal Linux Host :
    #   See core-x11 branch and
    #   https://groups.google.com/forum/#!topic/kivy-users/R4aJCph_7IQ
    # Others :
    #   Unknown, see
    #   - https://github.com/kivy/kivy/issues/4307
    #   - https://github.com/kivy/kivy/pull/5252
    _gui_supports_overlay_mode = False

    def __init__(self, *args, **kwargs):
        self._overlay_mode = None
        self._foundation_process = None
        super(OverlayWindowGuiMixin, self).__init__(*args, **kwargs)

    def install(self):
        super(OverlayWindowGuiMixin, self).install()
        _elements = {
            'overlay_mode': ElementSpec('display', 'overlay_mode', ItemSpec(bool, fallback=False)),
            'show_foundation': ElementSpec('display-rpi', 'show_foundation', ItemSpec(bool, fallback=True)),
            'dispmanx_foundation_layer': ElementSpec('display-rpi', 'dispmanx_foundation_layer', ItemSpec(int, fallback=1)),
            'foundation_image': ElementSpec('display-rpi', 'foundation_image', ItemSpec(fallback=None)),
        }
        for name, spec in _elements.items():
            self.config.register_element(name, spec)

    @property
    def overlay_mode(self):
        return self._overlay_mode

    @overlay_mode.setter
    def overlay_mode(self, value):
        if not self._gui_supports_overlay_mode and value:
            self.log.warn("Application tried to change overlay mode, "
                          "not supported this platform.")
            return
        if value is True:
            self._gui_overlay_mode_enter()
        else:
            self._gui_overlay_mode_exit()

    def _gui_overlay_mode_enter(self):
        self.log.info('Entering Overlay Mode')
        if self._overlay_mode:
            return
        self._overlay_mode = True
        Window.clearcolor = [0, 0, 0, 0]
        # self.gui_bg_pause()

    def _gui_overlay_mode_exit(self):
        self.log.info('Exiting Overlay Mode')
        if not self._overlay_mode:
            return
        self._overlay_mode = False
        # self.gui_bg_resume()
        Window.clearcolor = [0, 0, 0, 1]

    def stop(self):
        if self._foundation_process:
            self._foundation_process.terminate()
        super(OverlayWindowGuiMixin, self).stop()

    def gui_setup(self):
        super(OverlayWindowGuiMixin, self).gui_setup()

        if self.config.show_foundation and \
                self.config.foundation_image and \
                os.path.exists(self.config.foundation_image):
            cmd = ['pngview', '-l', str(self.config.dispmanx_foundation_layer),
                   '-n', self.config.foundation_image]
            self._foundation_process = subprocess.Popen(cmd)

        self.overlay_mode = self.config.overlay_mode