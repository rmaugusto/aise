import pickle
from map import Map


class GameContext():
    def __init__(self):
        self.map = Map()
        self.headless = False

class GameData(object):
    def __init__(self, brain, generation, training_time=0):
        self.brain = brain
        self.generation = generation
        self.training_time = training_time

    def save(self):
        with open('aise.gd', 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load(filename):
        with open('aise.gd', 'rb') as f:
            return pickle.load(f)
