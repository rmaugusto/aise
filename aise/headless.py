from aise import Aise
import time

class AiseHeadless():
    def __init__(self):
        self.aise = Aise()
        self.counter = 0
        self.update_time = time.time()

    def setup(self):

        self.aise.setup()

    def on_update(self, delta_time):
        self.aise.on_update(delta_time)
    
    def on_draw(self):
        distance = ""
        reward = ""

        if self.aise.best_fish is not None:
            distance = self.aise.best_fish.distance
            reward = self.aise.best_fish.reward.total

        print(f'{self.counter} fps, gen: {self.aise.generation}, dist: {distance}, reward: {reward}')

    def run(self):
        while True:
            self.counter += 1
            self.on_update( 1 / self.counter)

            if time.time() - self.update_time >= 1:
                self.on_draw()
                self.counter = 0
                self.update_time = time.time()

