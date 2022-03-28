

import os
import faulthandler

from ebs.linuxnode.gui.kivy.utils.launcher import prepare_config
from ebs.linuxnode.gui.kivy.utils.launcher import prepare_environment
from ebs.linuxnode.gui.kivy.utils.launcher import prepare_kivy


def run_node():
    nodeconfig = prepare_config('iotnode-kivy-example')

    prepare_environment(nodeconfig)
    prepare_kivy(nodeconfig)

    from ebs.linuxnode.core import config
    config.current_config = nodeconfig

    from ebs.linuxnode.gui.kivy.utils.application import BaseIOTNodeApplication

    class ExampleApplication(BaseIOTNodeApplication):
        def build(self):
            # This is an emergency-only approach. In general, configure
            # roots in the appropriate node classes instead.
            # ( for ex, see BaseIoTNodeGui.install() )
            r = super(ExampleApplication, self).build()
            self._config.register_application_root(
                os.path.abspath(os.path.dirname(__file__))
            )
            return r

        def on_start(self):
            # Config is ready by this point, as long as config elements and
            # application roots are all registered in the install()
            # call-chain.
            self._config.print()
            # Application Roots should also be ready before this
            super(ExampleApplication, self).on_start()

    print("Creating Application : {}".format(ExampleApplication))
    app = ExampleApplication(config=nodeconfig)
    app.run()


if __name__ == '__main__':
    print("Starting faulthandler")
    faulthandler.enable()
    run_node()
