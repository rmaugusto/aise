from ursina import *

from context import AiseContext

class GameCamera(EditorCamera):
    def __init__(self):
        super().__init__(name='game_camera', eternal=True)
        camera.orthographic = False
        self.rotation_x = 35
        self.target_z = -64


class MainKeyboard(Entity):
    def __init__(self):
        super().__init__(name='main_keyboard', eternal=True)

    def input(self, key):
        if key == 'escape':
            exit()
    
    def update(self):
        pass

class Engine:
    def __init__(self, context: AiseContext):
        self.context = context
        self.app = Ursina(vsync=True)
        application.blender_paths['default'] = '/mnt/5b8060d4-429d-47f5-8887-06a347f6faff/apps/blender-3.1.2-linux-x64/blender'
        window.color = color.black
        # window.borderless = False
        # window.exit_button.visible = False
        # window.title = 'AISE - Artificial Intelligence Simulated Environment'

        MainKeyboard()
        self.camera = GameCamera()

        self.context.pm.init_plugins()
        self.context.pm.load_plugins()

    def run(self):
        self.app.run()
