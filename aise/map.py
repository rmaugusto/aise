import random
import arcade
import numpy as np
import constants

class Map():
    def __init__(self):
        self.map_height = 0
        self.map_width = 0
        self.map = None
        self.tile_width = None
        self.tile_height = None
        self.water_list = None
        self.grass_list = None
        self.map_width = None
        self.map_height = None
        self.map = None

    def load_map(self, map_name):
        tile_map = arcade.load_tilemap(map_name, 1)
        self.tile_width = tile_map.tile_width
        self.tile_height = tile_map.tile_height

        self.water_list = tile_map.sprite_lists["water"]
        self.grass_list = tile_map.sprite_lists["grass"]

        self.map_width = tile_map.width * tile_map.tile_width
        self.map_height = tile_map.height * tile_map.tile_height

        self.map = np.full((self.map_width, self.map_height ), constants.MAP_TYPE_GRASS)

        # Marcar posições ocupadas com True
        for sprite in self.water_list:
            x = int(sprite.center_x - (self.tile_width / 2))
            x2 = int(x + self.tile_width)
            y = int(sprite.center_y - (self.tile_height / 2))
            y2 = int(y + self.tile_height)

            self.map[x:x2, y:y2] = constants.MAP_TYPE_LAKE

    def get_random_lake_position(self):
        i = random.randint(0,len(self.water_list)-1)
        return self.water_list[i].center_x, self.water_list[i].center_y

    def get_map(self, x, y):
        try:
            return self.map[int(x), int(y)]    
        except:
            return constants.MAP_TYPE_OUTSIDE
