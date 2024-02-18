from aise import Aise
import time
from aise import AbstractEventListener, EventNotification

class AiseHeadless(AbstractEventListener):
    def __init__(self):
        self.aise = Aise()
        self.aise.listener = self
        self.counter = 0
        self.update_time = time.time()

    def setup(self):
        self.aise.setup()

    def on_update(self, delta_time):
        self.aise.on_update(delta_time)
    
    def on_draw(self):
        print(f'{self.counter} fps, generation {self.aise.generation}')

    def on_event(self, notification: EventNotification):
        print(f'End of generation {notification.generation}, reward: {notification.best_fish.reward.total}, dist: {notification.best_fish.distance}')

    def run(self):
        while True:
            self.counter += 1
            self.on_update( 1 / self.counter)

            if time.time() - self.update_time >= 1:
                self.on_draw()
                self.counter = 0
                self.update_time = time.time()

