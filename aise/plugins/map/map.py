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

    def load(self):
        
        level = load_blender_scene('scenes_plane',
                                    load=True, 
                                    reload=False, 
                                    skip_hidden=True, 
                                    models_only=False
                                   )
        level.scale = Vec3(1,1,1)
        level.ground.texture='grass'
        level.ground.shader = lit_with_shadows_shader
        level.ground.enabled = False

        level.water.color = color.color(240, 1, 1, 0.6)
        level.water.shader = lit_with_shadows_shader
        level.water.enabled = True

        # print(level.water.bounds)
        # Entity(model='cube', scale=(1,1,1), position=level.water.world_position)
        # Entity(model='cube', position=level.water.position, scale=level.water.bounds, color=color.color(200,1,.8), double_sided=True)

        pass
                
    def unload(self):
        pass

    def destroy(self):
        pass