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
        print(f'{self.counter} fps, gen: {self.aise.generation}, dist: {self.aise.best_fish.distance}, reward: {self.aise.best_fish.reward.total}')

    def run(self):
        while True:
            self.counter += 1
            self.on_update( 1 / self.counter)

            if time.time() - self.update_time >= 1:
                self.on_draw()
                self.counter = 0
                self.update_time = time.time()

