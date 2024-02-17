
import arcade
from window import AiseWindow
from headless import AiseHeadless
import sys
import signal

cprofile = False 
headless = False
running_mode = False

def handler(signum, frame):
    res = input("Ctrl-c was pressed. Do you really want to exit? y/n ")
    if res == 'y':
        end_dump()
        exit(0)

def init_dump():
    if globals()["cprofile"]:
        globals()["cprofile"].enable()

def end_dump():
    if globals()["cprofile"]:
        import pstats
        globals()["cprofile"].disable()
        stats = pstats.Stats(globals()["cprofile"]).sort_stats('ncalls')
        stats = pstats.Stats(globals()["cprofile"])
        stats.dump_stats('aise.prof')

def main():

    if headless:        
        game = AiseHeadless()
        game.aise.game_context.headless = True
        game.aise.game_context.running_mode = running_mode
        game.setup()
        game.run()
    else:
        game = AiseWindow()
        game.aise.game_context.headless = False
        game.aise.game_context.running_mode = running_mode
        game.setup()
        arcade.run()

if __name__ == "__main__":

    globals()["headless"] = ('--headless') in sys.argv
    globals()["running_mode"] = ('--running-mode') in sys.argv

    if '--cprofile' in sys.argv :
        import cProfile
        globals()["cprofile"] = cProfile.Profile()

    signal.signal(signal.SIGINT, handler)
    
    init_dump()
    main()
    end_dump()