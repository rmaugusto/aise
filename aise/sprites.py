import math
import arcade
import numpy as np
from reward import Reward

from ray_casting import RayCasting

MIN_FISH_SPEED = 1
MAX_FISH_SPEED = 10
FISH_ROTATION_SPEED = 5
TEXTURE_CHANGE_INTERVAL = 0.4
INITIAL_ENERGY = 1000

class Fish(arcade.Sprite):
    def __init__(self, id=-1, scale=0.5, x=0, y=0, angle=0, ray_casting=None, brain=None):
        super().__init__(scale=scale, center_x=x, center_y=y)
        self.id = id
        self.angle = angle
        self.collided = False
        self.alive = True
        self.speed = MIN_FISH_SPEED
        self.textures = arcade.load_spritesheet("assets/sprites/fish.png", 95, 95, 1, 12)
        self.texture_idx = 0
        self.animation_direction = 1
        self.texture_change_timer = 0
        self.distance = 0
        self.set_texture(self.texture_idx)
        self.sensor = ray_casting
        self.brain = brain
        self.reward = Reward(self)

    def rotate_left(self):
        self.angle += FISH_ROTATION_SPEED
        self.angle = self.angle % 360
        #self.energy -= FISH_ROTATION_SPEED

    def rotate_right(self):
        self.angle -= FISH_ROTATION_SPEED
        self.angle = self.angle % 360
        #self.energy -= FISH_ROTATION_SPEED

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

    def update(self, delta_time: float = 1 / 60):

        if self.alive:

            self.update_texture(delta_time)

            input = [self.distance, self.reward.total] + self.sensor.ray_distance
            sensor_input = np.array(input).reshape(-1, 1)

            decision = self.brain.forward(sensor_input)

#            if decision[0] > 0:
#                self.speed_up()
#
#            if decision[1] > 0:
#                self.slow_down()

            if decision[2] > 0:
                self.rotate_right()

            if decision[3] > 0:
                self.rotate_left()

            self.forward()

            if decision[2] <= 0 and decision[3] <= 0:
                self.distance += self.speed

            self.sensor.cast_rays(self.angle, self.center_x, self.center_y)
            
            if self.sensor.min_distance <= 10:
                self.collided = True

            self.reward.update()

        if (self.alive and self.collided):
            self.alive = False

        if self.reward.total < 0:
            self.alive = False

        return super().update()


    def update_texture(self, delta_time):
        self.texture_change_timer += delta_time * self.speed

        if self.texture_change_timer >= TEXTURE_CHANGE_INTERVAL:
            self.texture_change_timer = 0 
            self.texture_idx += self.animation_direction

            if self.texture_idx > 2 or self.texture_idx < 0:
                self.animation_direction *= -1
                self.texture_idx += self.animation_direction * 2

            self.set_texture(self.texture_idx)
    
    def draw(self, *, filter=None, pixelated=None, blend_function=None):
        r = super().draw(filter=filter, pixelated=pixelated, blend_function=blend_function)
        
        #self.sensor.draw() 

        return r
