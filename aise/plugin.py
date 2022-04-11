from abc import ABC, abstractmethod

from context import AiseContext
from ursina import Entity


class GenericPlugin(ABC, Entity):

    def __init__(self, aise_context: AiseContext) -> None:
        super().__init__()
        self.priority = 100
        self.aise_context = aise_context

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def unload(self):
        pass

    @abstractmethod
    def destroy(self):
        pass
