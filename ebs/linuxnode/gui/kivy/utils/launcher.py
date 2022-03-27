

import os
from raspi_system import hwinfo

from ebs.linuxnode.core.config import ItemSpec
from ebs.linuxnode.core.config import ElementSpec


def prepare_config(appname):
    from ebs.linuxnode.core.config import IoTNodeConfig
    node_config = IoTNodeConfig(appname=appname)

    for name, spec in [
        ('platform', ElementSpec('platform', 'platform', ItemSpec(fallback='native'))),
        ('fullscreen', ElementSpec('display', 'fullscreen', ItemSpec(bool, fallback=True))),
        ('portrait', ElementSpec('display', 'portrait', ItemSpec(bool, fallback=False))),
        ('flip', ElementSpec('display', 'flip', ItemSpec(bool, fallback=False))),
        ('app_dispmanx_layer', ElementSpec('display-rpi', 'dispmanx_app_layer', ItemSpec(int, fallback=5)))
    ]:
        node_config.register_element(name, spec)

    return node_config


def prepare_environment(node_config):

    os.environ['KIVY_TEXT'] = 'pango'
    os.environ['KIVY_VIDEO'] = 'ffpyplayer'

    if node_config.platform == 'rpi':
        if hwinfo.is_pi4():
            os.environ['KIVY_WINDOW'] = 'sdl2'
        else:
            os.environ['KIVY_WINDOW'] = 'egl_rpi'
        os.environ['KIVY_BCM_DISPMANX_LAYER'] = str(node_config.app_dispmanx_layer)
        print("Using app_dispmanx_layer {0}".format(node_config.app_dispmanx_layer))


def prepare_kivy(node_config):
    from kivy.config import Config
    if node_config.fullscreen is True:
        Config.set('graphics', 'fullscreen', 'auto')

    # if config.current_config.orientation:
    #     Config.set('graphics', 'rotation', nodeconfig.orientation)

    Config.set('kivy', 'keyboard_mode', 'systemandmulti')

    from kivy.support import install_twisted_reactor
    install_twisted_reactor()
