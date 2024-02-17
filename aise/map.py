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



    def is_adjacent_water(self, sprite, water_list, direction, tile_width, tile_height):
        # Direções consideradas
        dx, dy = 0, 0
        if direction == 'left':
            dx = -tile_width
        elif direction == 'right':
            dx = tile_width
        elif direction == 'up':
            dy = -tile_height
        elif direction == 'down':
            dy = tile_height

        for water_sprite in water_list:
            if (water_sprite.center_x == sprite.center_x + dx and
                    water_sprite.center_y == sprite.center_y + dy):
                return True
        return False

    def get_random_lake_position_with_buffer(self):
        while True:
            i = random.randint(0, len(self.water_list)-1)
            selected_sprite = self.water_list[i]

            # Verificar por sprites de água em todas as direções
            directions = ['left', 'right', 'up', 'down']
            has_water_all_around = all(self.is_adjacent_water(selected_sprite, self.water_list, dir, self.tile_width, self.tile_height) for dir in directions)

            if has_water_all_around:
                return selected_sprite.center_x, selected_sprite.center_y
            else:
                # Ajustar a posição se não houver água em todas as direções
                adjustments = {'left': (100, 0), 'right': (-100, 0), 'up': (0, 100), 'down': (0, -100)}
                for dir in directions:
                    if not self.is_adjacent_water(selected_sprite, self.water_list, dir, self.tile_width, self.tile_height):
                        dx, dy = adjustments[dir]
                        return selected_sprite.center_x + dx, selected_sprite.center_y + dy

    def get_map(self, x, y):
        try:
            return self.map[int(x), int(y)]    
        except:
            return constants.MAP_TYPE_OUTSIDE
