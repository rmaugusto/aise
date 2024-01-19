import arcade
from panel import TextPanel
from neural_network import NeuralNetwork
from thread import ThreadPool
from game_context import GameContext
from sprites import Fish
from ray_casting import RayCasting
from operator import itemgetter

TOTAL_FISHES = 80

SENSOR_COUNT = 6
SENSOR_MAX_DISTANCE = 100

BRAIN_SIZE_INPUT = 1 + 1 + SENSOR_COUNT
BRAIN_SIZE_HIDDEN = 6
BRAIN_SIZE_OUTPUT = 4

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
        self.generation = 1
        self.fishes = []
        self.best_brain = None
        self.text_panel = TextPanel(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.pool = ThreadPool(10)
        self.best_fish = None

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

        self.game_context.map.load_map("assets/map/map.tmx")

        self.restart()

    def restart(self):
        self.fishes = []

        x, y = self.game_context.map.get_random_lake_position()
        for i in range(TOTAL_FISHES):
            sensor = RayCasting(SENSOR_COUNT,SENSOR_MAX_DISTANCE,self.game_context)

            if self.best_brain:
                brain = self.best_brain.clone()
                brain.mutate_randomly()
            else:
                brain = NeuralNetwork([BRAIN_SIZE_INPUT, BRAIN_SIZE_HIDDEN, BRAIN_SIZE_HIDDEN, BRAIN_SIZE_OUTPUT],'relu')

            fish = Fish(id=i,angle=0,ray_casting=sensor,brain=brain)
            fish.center_x = x
            fish.center_y = y

            self.fishes.append(fish)

    def update_fish(self, fish, delta_time):

        fish.update(delta_time)

    def on_update(self, delta_time):
        pass
        all_dead = True

        for fish in self.fishes:
            if fish.alive:
                all_dead = False
                self.pool.add_task(self.update_fish, fish, delta_time)
                #self.update_fish(fish)

        self.pool.wait_completion()

        self.fishes.sort(key=lambda x: x.reward.total, reverse=True)

        best_fish_alive = self.fishes[0]
        self.best_fish  = best_fish_alive

        for f in self.fishes:
            if f.reward.total > self.best_fish.reward.total:
                self.best_fish = f

                if f.alive:
                    best_fish_alive = f

        #best_fish_alive = max(filter(lambda f: f.alive, self.fishes), key=lambda f: f.reward.total)
        #self.best_fish = max(self.fishes, key=lambda f: f.reward.total)

        if all_dead:
            self.end_generation()
            self.restart()

        self.text_panel.set_text(0, f"Geração: {self.generation}")

        pos = 0
        for i in range(0,5):
            f = self.fishes[i]
            pos += 1
            self.text_panel.set_text(pos, f"Pos #{i} - #{f.id}")
            pos += 1
            self.text_panel.set_text(pos, f"-> Reward: {f.reward.total}, Dist: {f.distance}")

        #self.text_panel.set_text(1, f"Melhor - #{self.best_fish.id}")
        #self.text_panel.set_text(2, f"-> Reward: {self.best_fish.reward.total}, Dist: {self.best_fish.distance}")
        #self.text_panel.set_text(3, f"Melhor vivo - #{best_fish_alive.id}")
        #self.text_panel.set_text(4, f"-> Reward: {best_fish_alive.reward.total}, Dist: {best_fish_alive.distance}")

    def end_generation(self):
        self.best_brain = self.best_fish.brain
        self.generation += 1
    
    def on_draw(self):

        self.clear()

        arcade.start_render()

        self.perf_graph_list.draw()

        self.game_context.map.water_list.draw()
        self.game_context.map.grass_list.draw()

        for fish in self.fishes:
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
