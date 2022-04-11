
from plugin_manager import PluginManager


class AiseContext:

    def __init__(self):
        self.pm = PluginManager(self)
        self.map = None
