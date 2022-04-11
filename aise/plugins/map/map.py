from context import AiseContext
from plugin import GenericPlugin
from ursina.shaders import basic_lighting_shader, colored_lights_shader, lit_with_shadows_shader
from ursina import *
from panda3d.core import CollisionEntry

class MapPlugin(GenericPlugin):

    def __init__(self, aise_context: AiseContext):
        super().__init__(aise_context)
        self.priority = 10
        pass

    def init(self):
        pass

    def input(self, key):
        if key == 'g':
           self.aise_context.map.ground.visible = not self.aise_context.map.ground.visible 

    def load(self):
        
        level = load_blender_scene('scenes_plane',
                                    load=True, 
                                    reload=False, 
                                    skip_hidden=True, 
                                    models_only=False
                                   )
        level.scale = Vec3(1,1,1)
        level.collider = None
        level.ground.texture='grass'
        level.ground.shader = lit_with_shadows_shader
        level.ground.enabled = True
        level.ground.collider = 'mesh'

        level.water.color = color.color(240, 1, 1, 0.3)
        level.water.shader = lit_with_shadows_shader
        level.water.enabled = True
        level.water.collider = None

        self.aise_context.map = level
        pass
                
    def unload(self):
        pass

    def destroy(self):
        pass