class PluginManager:

    def __init__(self, context):
        from plugins.fish.fish import FishPlugin
        from plugins.map.map import MapPlugin
        self.plugins = [FishPlugin(context), MapPlugin(context)]
        self.plugins.sort(key=lambda x: x.priority)

    def init_plugins(self):
        [p.init for p in self.plugins]

    def load_plugins(self):
        [p.load() for p in self.plugins]

    def unload_plugins(self):
        [p.unload() for p in self.plugins]

    def destroy_plugins(self):
        [p.destroy() for p in self.plugins]
