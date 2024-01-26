import pickle
from map import Map


class GameContext():
    def __init__(self):
        self.map = Map()
        self.headless = False

class GameData(object):
    def __init__(self):
        self.brain = None
        self.generation = None
        self.training_time = 0

    def save(self):
        with open('aise.gd', 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load():
        with open('aise.gd', 'rb') as f:
            return pickle.load(f)
