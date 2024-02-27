from abc import ABC


class EventNotification():
    def __init__(self):
        self.best_fish = None
        self.generation = 0

class AbstractEventListener(ABC):
    def on_event(self, notification: EventNotification):
        pass
