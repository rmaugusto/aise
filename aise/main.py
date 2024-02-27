from contextlib import contextmanager
import arcade
from window import AiseWindow
from training import TrainingHeadless
import signal
import copy
from yaml import load, Loader

# Use argparse for cleaner argument parsing
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--mode", choices=["training", "simulation"], default=None, help="Running mode")
parser.add_argument("--cprofile", action="store_true", help="Enable profiling")
args = parser.parse_args()

# Declare variables for clarity
mode = args.mode
cprofile = args.cprofile

class ConfigObject:
    def __init__(self, **entries): 
        self.__dict__.update(entries)    

    def is_training(self):
        return self.mode == "training"

    @classmethod
    def from_dict(cls, data):
        if isinstance(data, dict):
            return cls(**{k: cls.from_dict(v) for k, v in data.items()})
        else:
            return data

    def clone(self):
        return copy.deepcopy(self)

# Define a context manager for profiling
@contextmanager
def profiling():
    if cprofile:
        import cProfile
        profiler = cProfile.Profile()
        profiler.enable()
        try:
            yield
        finally:
            profiler.disable()
            import pstats
            stats = pstats.Stats(profiler).sort_stats('ncalls')
            stats.dump_stats('aise.prof')
    else:
        yield  # No-op if profiling is disabled


def main():

    with open('assets/config.yaml', 'r') as f:
        config = load(f, Loader=Loader)

    #convert config to python object
    config_obj = ConfigObject.from_dict(config)

    #priority to args over config
    if cprofile:
        config_obj.cprofile = True

    if mode:
        config_obj.mode = mode


    with profiling():  # Employ the context manager

        if config_obj.is_training():
            game = TrainingHeadless(config_obj)
        else:
            game = AiseWindow()

        game.config = config_obj
        game.setup()

        if config_obj.is_training():
            game.run()
        else:
            arcade.run()  # Let arcade handle the main loop

if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda signum, frame: exit())  # Simpler exit handling
    main()