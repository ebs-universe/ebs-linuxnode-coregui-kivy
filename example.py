

import faulthandler

import os
from raspi_system import hwinfo

from ebs.linuxnode.core.config import ItemSpec
from ebs.linuxnode.core.config import ElementSpec


def run_node():
    from ebs.linuxnode.core.config import IoTNodeCoreConfig
    nodeconfig = IoTNodeCoreConfig()

    for name, spec in [
        ('platform', ElementSpec('platform', 'platform', ItemSpec(fallback='native'))),
        ('fullscreen', ElementSpec('display', 'fullscreen', ItemSpec(bool, fallback=True))),
        ('portrait', ElementSpec('display', 'portrait', ItemSpec(bool, fallback=False))),
        ('flip', ElementSpec('display', 'flip', ItemSpec(bool, fallback=False))),
        ('app_dispmanx_layer', ElementSpec('display-rpi', 'dispmanx_app_layer', ItemSpec(int, fallback=5)))
    ]:
        nodeconfig.register_element(name, spec)

    from ebs.linuxnode.core import config
    config.current_config = nodeconfig

    os.environ['KIVY_TEXT'] = 'pango'
    os.environ['KIVY_VIDEO'] = 'ffpyplayer'

    if nodeconfig.platform == 'rpi':
        if hwinfo.is_pi4():
            os.environ['KIVY_WINDOW'] = 'sdl2'
        else:
            os.environ['KIVY_WINDOW'] = 'egl_rpi'
        os.environ['KIVY_BCM_DISPMANX_LAYER'] = str(nodeconfig.app_dispmanx_layer)
        print("Using app_dispmanx_layer {0}".format(nodeconfig.app_dispmanx_layer))

    from kivy.config import Config
    if nodeconfig.fullscreen is True:
        Config.set('graphics', 'fullscreen', 'auto')

    # if nodeconfig.orientation:
    #     Config.set('graphics', 'rotation', nodeconfig.orientation)

    Config.set('kivy', 'keyboard_mode', 'systemandmulti')

    from kivy.support import install_twisted_reactor
    install_twisted_reactor()

    from ebs.linuxnode.gui.kivy.core.application import BaseIOTNodeApplication
    print("Starting Application")
    BaseIOTNodeApplication(config=nodeconfig).run()


if __name__ == '__main__':
    print("Starting faulthandler")
    faulthandler.enable()
    run_node()
