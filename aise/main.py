import math
import arcade
import numpy as np
from random import randrange
from game_context import GameContext
from sprites import Fish
from ray_casting import RayCasting
import constants

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1000

GRAPH_WIDTH = 200
GRAPH_HEIGHT = 120
GRAPH_MARGIN = 5

arcade.enable_timings()

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "AISE")
        self.game_context = GameContext()
        self.physics_engine = None
        self.frame_count = 0

        
        #self.wall_sprite = arcade.SpriteSolidColor(800,600,arcade.color.WHITE)
        #self.wall_sprite.center_x = MAP_WIDTH/2
        #self.wall_sprite.center_y = MAP_HEIGHT/2

        #self.wall = np.full((int(MAP_WIDTH), int(MAP_HEIGHT)), 1)
        #x = int(self.wall_sprite.center_x - (self.wall_sprite.width/2))
        #y = int(self.wall_sprite.center_y - (self.wall_sprite.height/2))
        #dx = int(self.wall_sprite.center_x + (self.wall_sprite.width/2))
        #dy = int(self.wall_sprite.center_y + (self.wall_sprite.height/2))
        #self.wall[ x:dx, y:dy ] = 0 


    def setup(self):

        self.perf_graph_list = arcade.SpriteList()

        graph = arcade.PerfGraph(GRAPH_WIDTH, GRAPH_HEIGHT, graph_data="FPS")
        graph.center_x = GRAPH_WIDTH / 2
        graph.center_y = self.height - GRAPH_HEIGHT / 2
        self.perf_graph_list.append(graph)

        graph = arcade.PerfGraph(GRAPH_WIDTH, GRAPH_HEIGHT, graph_data="update")
        graph.center_x = GRAPH_WIDTH / 2 + (GRAPH_WIDTH + GRAPH_MARGIN)
        graph.center_y = self.height - GRAPH_HEIGHT / 2
        self.perf_graph_list.append(graph)

        graph = arcade.PerfGraph(GRAPH_WIDTH, GRAPH_HEIGHT, graph_data="on_draw")
        graph.center_x = GRAPH_WIDTH / 2 + (GRAPH_WIDTH + GRAPH_MARGIN) * 2
        graph.center_y = self.height - GRAPH_HEIGHT / 2
        self.perf_graph_list.append(graph)


        map_name = "assets/map/map.tmx"

        self.tile_map = arcade.load_tilemap(map_name, 1)
        self.water_list = self.tile_map.sprite_lists["water"]
        self.grass_list = self.tile_map.sprite_lists["grass"]

        self.game_context.map_width = self.tile_map.width * self.tile_map.tile_width
        self.game_context.map_height = self.tile_map.height * self.tile_map.tile_height
        

        # Criar um array NumPy inicializado com False
        self.game_context.map = np.full((self.game_context.map_width, self.game_context.map_height ), constants.MAP_TYPE_GRASS)

        # Marcar posições ocupadas com True
        for sprite in self.water_list:
            x = int(sprite.center_x - (self.tile_map.tile_width / 2))
            x2 = int(x + self.tile_map.tile_width)
            y = int(sprite.center_y - (self.tile_map.tile_height / 2))
            y2 = int(y + self.tile_map.tile_height)

            self.game_context.map[x:x2, y:y2] = constants.MAP_TYPE_LAKE


        self.fish = Fish(angle=0,ray_casting=RayCasting(6,100,self.game_context))
        self.fish.center_x = 800
        self.fish.center_y = 100



        self.post_setup()

    def post_setup(self):
        pass

    def on_update(self, delta_time):
        self.fish.forward()
        self.fish.update()

    def on_draw(self):

        self.clear()

        arcade.start_render()

        self.perf_graph_list.draw()

        self.water_list.draw()
        self.grass_list.draw()

        self.fish.draw()

        arcade.finish_render()

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        pass
            
    def on_resize(self, width, height):
        super().on_resize(width, height)


    def on_key_press(self, key, modifiers):
        pass
        #if key == arcade.key.LEFT:

    def on_key_release(self, key, modifiers):
        pass
        #if key == arcade.key.UP:
        #    self.best_car.stop()
        #if key == arcade.key.LEFT:
        #    self.best_car.rotating_left = False
        #if key == arcade.key.RIGHT:
        #    self.best_car.rotating_right = False


def main():
    game = MyGame()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    import cProfile, pstats
    profiler = cProfile.Profile()
    profiler.enable()
    main()
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('ncalls')
    stats = pstats.Stats(profiler)
    stats.dump_stats('aise.prof')
