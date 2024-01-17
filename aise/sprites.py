import math
import arcade

from ray_casting import RayCasting

MIN_FISH_SPEED = 1
MAX_FISH_SPEED = 10
FISH_ROTATION_SPEED = 5

class Fish(arcade.Sprite):
    def __init__(self, id=-1, scale=0.5, x=0, y=0, angle=0, ray_casting=None):
        super().__init__(scale=scale, center_x=x, center_y=y)
        self.id = id
        self.angle = angle
        self.collided = False
        self.distance = 0
        self.manual = False
        self.speed = MIN_FISH_SPEED
        texture = arcade.load_spritesheet("assets/sprites/fish.png", 95, 95, 1, 12)
        self.textures = texture
        self.set_texture(0)
        self.sensor = ray_casting


    def rotate_left(self):
        self.angle += FISH_ROTATION_SPEED
        self.angle = self.angle % 360

    def rotate_right(self):
        self.angle -= FISH_ROTATION_SPEED
        self.angle = self.angle % 360

    def speed_up(self):
        if self.speed < MAX_FISH_SPEED:
            self.speed += 0.5

    def slow_down(self):
        if self.speed > MIN_FISH_SPEED:
            self.speed -= 0.5

    def forward(self):

        angle_rad = math.radians(self.angle)
        self.center_x += self.speed * math.cos(angle_rad)
        self.center_y += self.speed * math.sin(angle_rad)

    def stop(self):
        self.change_x = 0
        self.change_y = 0

    def update(self):

        if not self.collided:

            #if self.manual:
            #    if self.rotating_right:
            #        self.rotate_right()
#
            #    if self.rotating_left:
            #        self.rotate_left()
#
#
            #self.forward()

            self.sensor.cast_rays(self.angle, self.center_x, self.center_y)


        return super().update()

    def draw(self, *, filter=None, pixelated=None, blend_function=None):
        r = super().draw(filter=filter, pixelated=pixelated, blend_function=blend_function)
        
        self.sensor.draw() 

        return r
