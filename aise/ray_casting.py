
import math

import arcade

import constants

from numba import njit

RAYS_COUNT = 7

class RayCasting:
    def __init__(self, num_rays=18, max_distance=200, gc=None):
        self.num_rays = num_rays
        self.ray_distance = [max_distance] * num_rays
        self.ray_start_points = [(0, 0)] * num_rays
        self.ray_end_points = [(0, 0)] * num_rays
        self.max_distance = max_distance
        self.min_distance = max_distance
        self.gc = gc

    def cast_rays(self, entity_angle, center_x, center_y):
        
        for i in range(self.num_rays):
            angle = entity_angle - 90.0 + (i)*180.0/((RAYS_COUNT-2))
            self.cast_single_ray(i, angle, center_x, center_y)
            self.min_distance = min(self.min_distance, self.ray_distance[i])

    def cast_single_ray(self, idx, angle,center_x, center_y):

        angle_rad = math.radians(angle)
        start_x, start_y = center_x, center_y

        try:
            if self.gc.map.get_map(start_x, start_y) in (constants.MAP_TYPE_GRASS, constants.MAP_TYPE_OUTSIDE):
                self.set_ray_data(idx, start_x, start_y, start_x,start_y,0)
                return
        except Exception as e:
            return

        step_size = 10
        reached = False

        for distance in range(0, self.max_distance, step_size):
            end_x = start_x + distance * math.cos(angle_rad)
            end_y = start_y + distance * math.sin(angle_rad)

            if self.gc.map.get_map(end_x, end_y) in (constants.MAP_TYPE_GRASS, constants.MAP_TYPE_OUTSIDE):
                reached = True
                self.set_ray_data(idx, start_x, start_y, end_x, end_y, distance)
                break

        if not reached:
            self.set_ray_data(idx, start_x, start_y, end_x, end_y, distance)

    def set_ray_data(self, idx, start_x, start_y, end_x, end_y, distance):
        self.ray_start_points[idx] = (start_x, start_y)
        self.ray_end_points[idx] = (end_x, end_y)
        self.ray_distance[idx] = distance

    def draw(self):
        for i in range(self.num_rays):            
            arcade.draw_line(self.ray_start_points[i][0], self.ray_start_points[i][1], self.ray_end_points[i][0], self.ray_end_points[i][1], arcade.color.RED, 1)
            arcade.draw_circle_filled(self.ray_end_points[i][0], self.ray_end_points[i][1],6,arcade.color.RED)
