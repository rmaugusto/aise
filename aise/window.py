import arcade
from aise import Aise
from graph import AiseGraph
from panel import TextPanel


SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1000

GRAPH_WIDTH = 200
GRAPH_HEIGHT = 120
GRAPH_MARGIN = 5

arcade.enable_timings()

class AiseWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "AISE")
        self.aise = Aise()
        self.physics_engine = None
        self.text_panel = TextPanel(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.br_graph = AiseGraph(GRAPH_WIDTH, GRAPH_HEIGHT,graph_data="Rewards",data_to_graph= self.aise.best_fish_rewards)

    def setup(self):

        self.perf_graph_list = arcade.SpriteList()

        graph = arcade.PerfGraph(GRAPH_WIDTH, GRAPH_HEIGHT, graph_data="FPS")
        graph.center_x = GRAPH_WIDTH / 2
        graph.center_y = self.height - GRAPH_HEIGHT / 2
        self.perf_graph_list.append(graph)

        graph = arcade.PerfGraph(GRAPH_WIDTH, GRAPH_HEIGHT, graph_data="on_draw")
        graph.center_x = GRAPH_WIDTH / 2 + (GRAPH_WIDTH + GRAPH_MARGIN) 
        graph.center_y = self.height - GRAPH_HEIGHT / 2
        self.perf_graph_list.append(graph)

        graph = self.br_graph
        graph.center_x = GRAPH_WIDTH / 2 + (GRAPH_WIDTH + GRAPH_MARGIN) * 2
        graph.center_y = self.height - GRAPH_HEIGHT / 2
        self.perf_graph_list.append(graph)

        self.aise.setup()

    def update_text_panel(self):
        self.text_panel.set_text(0, f"Geração: {self.aise.generation}")

        pos = 0
        for i in range(0,5):
            f = self.aise.fishes[i]
            pos += 1
            self.text_panel.set_text(pos, f"Pos #{i} - #{f.id}")
            pos += 1
            self.text_panel.set_text(pos, f"-> Reward: {f.reward.total}, Dist: {f.distance}")

    def on_update(self, delta_time):

        self.aise.on_update(delta_time)
        self.update_text_panel()

    def on_draw(self):

        self.clear()

        arcade.start_render()

        self.perf_graph_list.draw()

        self.aise.game_context.map.water_list.draw()
        self.aise.game_context.map.grass_list.draw()

        for fish in self.aise.fishes:
            if fish.alive:
                fish.draw()

        self.text_panel.draw()

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

