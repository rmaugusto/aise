from typing import List
import arcade
from graph import AiseGraph, AiseMGraph
from panel import TextPanel
from neural_network import NeuralNetwork
from thread import ThreadPool
from game_context import GameContext
from sprites import Fish
from ray_casting import RayCasting

TOTAL_FISHES = 20
TOTAL_UPDATE_THREADS = 10

SENSOR_COUNT = 6
SENSOR_MAX_DISTANCE = 100

BRAIN_SIZE_INPUT = 1 + 1 + SENSOR_COUNT
BRAIN_SIZE_HIDDEN = 6
BRAIN_SIZE_OUTPUT = 4

#1845

class Aise():
    def __init__(self):
        self.game_context = GameContext()
        self.generation = 1
        self.fishes = []
        self.best_brain = None
        self.pool = ThreadPool(TOTAL_UPDATE_THREADS)
        self.best_fish = None
        self.best_fish_rewards: List[float] = []
        self.best_fish_distance= []

    def setup(self):

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

        self.pool.wait_completion()

        self.fishes.sort(key=lambda x: x.reward.total, reverse=True)

        best_fish_alive = self.fishes[0]
        self.best_fish  = best_fish_alive

        for f in self.fishes:
            #if f.reward.total > self.best_fish.reward.total:
            if f.distance > self.best_fish.distance:
                self.best_fish = f

                if f.alive:
                    best_fish_alive = f

        if all_dead:
            self.end_generation()
            self.restart()



    def end_generation(self):
        
        self.best_fish_rewards.append(self.best_fish.reward.total)
        self.best_fish_distance.append(self.best_fish.distance)

        self.best_brain = self.best_fish.brain
        self.generation += 1
    
    def on_draw(self):
        pass



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
