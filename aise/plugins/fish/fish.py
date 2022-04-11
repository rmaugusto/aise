from context import AiseContext
from plugin import GenericPlugin
from ursina import *
from direct.actor.Actor import Actor

class FishPlugin(GenericPlugin):

    def __init__(self, aise_context: AiseContext):
        super().__init__(aise_context)
        pass

    def init(self):
        pass

    def load(self):
        anima = Entity(name='f', model='fish',position=Vec3(0,10,0), texture='fish_texture')

        pass

    def unload(self):
        pass

    def destroy(self):
        pass