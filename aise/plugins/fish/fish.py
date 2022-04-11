from context import AiseContext
from plugin import GenericPlugin
from ursina import *
from direct.actor.Actor import Actor
from random import uniform

class Fish(Entity):
    def __init__(self, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities, **kwargs)

    def update(self):
        self.position -= self.forward * time.dt * 5
        hit_info = self.intersects()
        if hit_info.hit:
            destroy(self)

class FishPlugin(GenericPlugin):

    def __init__(self, aise_context: AiseContext):
        super().__init__(aise_context)
        pass

    def init(self):
        pass

    def load(self):
        # fishes = []
        
        for i in range(30):
            f = self.create_fish()

        pass

    def input(self, key):
        if key == 'b':
            for i in range(1):
                f = self.create_fish()


    def unload(self):
        pass

    def destroy(self):
        pass

    def click_on_fish(self, fish):
        h = fish.intersects()
        print(h.hit)

    def create_fish(self):
        wp = self.aise_context.map.water.position
        wb = self.aise_context.map.water.bounds
        created = False

        while not created:
            rnd_x = uniform(wp.x-(wb.x/2), wp.x+(wb.x/2))
            rnd_z = uniform(wp.z-(wb.z/2), wp.z+(wb.z/2))
            f = Fish(model='fish',position=(rnd_x,0,rnd_z), scale=0.4, collider='box')
            f.on_click = lambda: self.click_on_fish(f)
            f.rotation_y = uniform(0, 180)
            if f.intersects(self.aise_context.map.ground).hit:
                destroy(f)
            else:
                created = True
                f.texture='fish_texture'

        return f