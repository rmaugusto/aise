import random
import time
from typing import List
from game_context import GameContext
from agent import Fish
from ray_casting import RayCasting

class AiseTrainer():
    def __init__(self, config):
        self.game_context = GameContext()
        self.fishes = []
        self.best_brain = None
        self.best_fish = None
        self.config = config
        self.running = False
        self.elapsed_time = 0

    def load(self):
        self.game_context.map.load_map("assets/map/map.tmx")

    def configure(self, brain = None):
        self.best_fish = None
        self.best_brain = brain

    def start(self):
        self.fishes = []

        #x, y = self.game_context.map.get_random_lake_position()
        x, y = self.game_context.map.get_random_lake_position_with_buffer()

        random_angle = random.randint(0, 359)
        for i in range(self.config.training.agent_count):

            sensor = RayCasting(self.config.training.sensor_count,self.config.training.sensor_max_distance,self.game_context)

            brain = self.best_brain.clone()

            if i > 0:
                brain.mutate_randomly()
                    
            fish = Fish(id=i,angle=random_angle,ray_casting=sensor,brain=brain, game_context=self.game_context)
            fish.center_x = x
            fish.center_y = y

            self.fishes.append(fish)

        self.running = True


    def update_fish(self, fish, delta_time):
        fish.update(delta_time)

    def update(self, delta_time):
        all_dead = True

        for fish in self.fishes:
            if fish.alive:
                all_dead = False
                self.update_fish(fish, delta_time)

        if all_dead:
            self.end_generation()

    def end_generation(self):
        
        self.fishes.sort(key=lambda x: x.reward.total, reverse=True)
        self.best_fish = self.fishes[0]
        self.best_brain = self.best_fish.brain
        self.running = False
    

    def run_until_done(self):
        self.elapsed_time = 0
        start_time = time.time()
        self.start()
        while(self.running):
            self.update(1/60)

        self.elapsed_time = time.time() - start_time
        print(f"Elapsed time: {self.elapsed_time}")

        return self.best_fish