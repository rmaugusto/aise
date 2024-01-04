import math
import arcade
import numpy as np
from random import randrange, uniform

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1000
MAP_WIDTH = 1600
MAP_HEIGHT = 1000
RAY_CAR_COUNT = 18

GRAPH_WIDTH = 200
GRAPH_HEIGHT = 120
GRAPH_MARGIN = 5

arcade.enable_timings()

class RayCasting:
    def __init__(self, num_rays=18, max_distance=200):
        self.num_rays = num_rays
        self.ray_distance = [max_distance] * num_rays
        self.ray_start_points = [(0, 0)] * num_rays
        self.ray_end_points = [(0, 0)] * num_rays
        self.max_distance = max_distance
        self.min_distance = max_distance

    def cast_rays(self, walls, entity_angle, center_x, center_y):
        for i in range(self.num_rays):
            angle = entity_angle - 90.0 + (i)*360.0/((RAY_CAR_COUNT-2))
            self.cast_single_ray(i, angle, walls, center_x, center_y)
            self.min_distance = min(self.min_distance, self.ray_distance[i])

    def cast_single_ray(self, idx, angle, walls,center_x, center_y):

        angle_rad = math.radians(angle)
        start_x, start_y = center_x, center_y

        try:
            if walls[int(start_x), int(start_y)]:
                self.set_ray_data(idx, start_x, start_y, start_x,start_y,0)
                return
        except:
            return

        step_size = 10
        reached = False

        for distance in range(0, self.max_distance, step_size):
            end_x = start_x + distance * math.cos(angle_rad)
            end_y = start_y + distance * math.sin(angle_rad)

            if walls[int(end_x), int(end_y)] == 1:
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


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Arcade Car Game")
        self.physics_engine = None
        self.map_width = MAP_WIDTH
        self.map_height = MAP_HEIGHT

        self.wall_sprite = arcade.SpriteSolidColor(800,600,arcade.color.WHITE)
        self.wall_sprite.center_x = MAP_WIDTH/2
        self.wall_sprite.center_y = MAP_HEIGHT/2

        self.players = []

        

        for i in range(20):
            player = arcade.SpriteCircle(10,arcade.color.BLUE)
            player.center_x = randrange(self.wall_sprite.center_x - (self.wall_sprite.width/2), self.wall_sprite.center_x + (self.wall_sprite.width/2))
            player.center_y = randrange(self.wall_sprite.center_y - (self.wall_sprite.height/2), self.wall_sprite.center_y + (self.wall_sprite.height/2))
            player.sensor = RayCasting(18,200)
            self.players.append(player)

        self.wall = np.full((int(MAP_WIDTH), int(MAP_HEIGHT)), 1)
        x = int(self.wall_sprite.center_x - (self.wall_sprite.width/2))
        y = int(self.wall_sprite.center_y - (self.wall_sprite.height/2))
        dx = int(self.wall_sprite.center_x + (self.wall_sprite.width/2))
        dy = int(self.wall_sprite.center_y + (self.wall_sprite.height/2))
        self.wall[ x:dx, y:dy ] = 0 


    def setup(self):

        self.perf_graph_list = arcade.SpriteList()

        self.angle = 0
        self.angular_velocity = 0.1
        self.radius = 1


        # Create the FPS performance graph
        graph = arcade.PerfGraph(GRAPH_WIDTH, GRAPH_HEIGHT, graph_data="FPS")
        graph.center_x = GRAPH_WIDTH / 2
        graph.center_y = self.height - GRAPH_HEIGHT / 2
        self.perf_graph_list.append(graph)

        # Create the on_update graph
        graph = arcade.PerfGraph(GRAPH_WIDTH, GRAPH_HEIGHT, graph_data="update")
        graph.center_x = GRAPH_WIDTH / 2 + (GRAPH_WIDTH + GRAPH_MARGIN)
        graph.center_y = self.height - GRAPH_HEIGHT / 2
        self.perf_graph_list.append(graph)

        # Create the on_draw graph
        graph = arcade.PerfGraph(GRAPH_WIDTH, GRAPH_HEIGHT, graph_data="on_draw")
        graph.center_x = GRAPH_WIDTH / 2 + (GRAPH_WIDTH + GRAPH_MARGIN) * 2
        graph.center_y = self.height - GRAPH_HEIGHT / 2
        self.perf_graph_list.append(graph)

        self.post_setup()

    def post_setup(self):
        pass

    def on_update(self, delta_time):

        self.angle += self.angular_velocity

        for player in self.players:        

            player.center_x = player.center_x + self.radius * math.cos(self.angle)
            player.center_y = player.center_y + self.radius * math.sin(self.angle)
            player.angle += 1
            player.sensor.cast_rays(self.wall, player.angle, player.center_x, player.center_y)

    


    def on_draw(self):

        arcade.start_render()

        #arcade.draw_rectangle_filled(self.map_out[0],self.map_out[1],self.map_out[2],self.map_out[3],arcade.color.RED)
        #arcade.draw_rectangle_filled(self.map_in[0],self.map_in[1],self.map_in[2],self.map_in[3],arcade.color.WHITE)
        self.wall_sprite.draw()

        for player in self.players:        
            player.draw()
            player.sensor.draw() 

        self.perf_graph_list.draw()

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
