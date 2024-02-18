from abc import ABC
import random
from typing import List
from neural_network_pytorch import NeuralNetworkPyTorch
from neural_network import NeuralNetwork
from thread import ThreadPool
from game_context import GameContext, GameData
from sprites import Fish
from ray_casting import RayCasting

TOTAL_FISHES = 20
TOTAL_UPDATE_THREADS = 4

SENSOR_COUNT = 6
SENSOR_MAX_DISTANCE = 100

BRAIN_SIZE_INPUT = 1 + 1 + 1 + 1 + SENSOR_COUNT
BRAIN_SIZE_HIDDEN = 6
BRAIN_SIZE_OUTPUT = 4

#1845

class EventNotification():
    def __init__(self):
        self.best_fish = None
        self.generation = 0

class AbstractEventListener(ABC):
    def on_event(self, notification: EventNotification):
        pass

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
        self.game_data = GameData()
        self.listener = None

    def setup(self):

        self.game_context.map.load_map("assets/map/map.tmx")

        try:        
            gd = GameData.load()
            self.best_brain = gd.brain
            self.generation = gd.generation
        except:
            pass    

        self.restart()

    def restart(self):
        self.fishes = []

        #x, y = self.game_context.map.get_random_lake_position()
        x, y = self.game_context.map.get_random_lake_position_with_buffer()

        random_angle = random.randint(0, 359)
        total_fishes = 1 if self.game_context.running_mode else TOTAL_FISHES
        for i in range(total_fishes):
            sensor = RayCasting(SENSOR_COUNT,SENSOR_MAX_DISTANCE,self.game_context)

            if self.best_brain:
                brain = self.best_brain.clone()

                if not self.game_context.running_mode:
                    if i > 0:
                        brain.mutate_randomly()
                    
            else:
                brain = NeuralNetworkPyTorch([BRAIN_SIZE_INPUT, BRAIN_SIZE_HIDDEN, BRAIN_SIZE_HIDDEN, BRAIN_SIZE_OUTPUT],'relu')

            fish = Fish(id=i,angle=random_angle,ray_casting=sensor,brain=brain, game_context=self.game_context)
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
                self.update_fish(fish, delta_time)
                #self.pool.add_task(self.update_fish, fish, delta_time)

        self.pool.wait_completion()

        if not self.game_context.headless:
            self.fishes.sort(key=lambda x: x.reward.total, reverse=True)
            best_fish_alive = self.fishes[0]
            self.best_fish  = best_fish_alive

            for f in self.fishes:
                if f.reward.total > self.best_fish.reward.total:
                #if f.distance > self.best_fish.distance:
                    self.best_fish = f

                    if f.alive:
                        best_fish_alive = f

        if all_dead:
            self.end_generation()
            self.restart()

    def end_generation(self):
        
        if not self.game_context.running_mode:
            
            self.fishes.sort(key=lambda x: x.reward.total, reverse=True)
            self.best_fish = self.fishes[0]

            self.best_fish_rewards.append(self.best_fish.reward.total)
            self.best_fish_distance.append(self.best_fish.distance)

            self.best_brain = self.best_fish.brain
            self.generation += 1

            self.game_data.brain = self.best_brain
            self.game_data.generation = self.generation
            self.game_data.save()
    
        if self.listener:
            notification = EventNotification()
            notification.best_fish = self.best_fish
            notification.generation = self.generation
            self.listener.on_event(notification)


    def on_draw(self):
        pass


