
from context import AiseContext
from engine import Engine


if __name__ == '__main__':
    context = AiseContext()
    engine = Engine(context)
    engine.run()


