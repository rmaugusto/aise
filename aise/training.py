from contextlib import nullcontext
from aise import AiseTrainer
import time
import multiprocessing

from utils import Util
from game_context import GameData
#from neural_network_keras import NeuralNetwork
from neural_network_pytorch import NeuralNetwork

class TrainingHeadless():
    def __init__(self, config):
        self.instances = []
        self.threads = []
        self.update_time = time.time()
        self.config = config
        self.game_data = GameData()
        self.generation = 0
        self.best_brain = None
        self.best_fish = None

    def setup(self):

        try:        
            self.game_data = GameData.load()
            #self.generation = gd.generation
            self.best_brain = self.game_data.brain
        except:

            self.best_brain = NeuralNetwork(self.config)


        for i in range(self.config.training.instances):
            inst = AiseTrainer( self.config.clone() )
            inst.load()

            self.instances.append(inst)


    def executar_metodo_instancia(self, instancia):
        return instancia.run_until_done()

    def run(self):


            pool_count = None if self.config.training.pool_size == -1 else self.config.training.pool_size
            use_pool = False if self.config.training.pool_size == 0 else True

            with multiprocessing.Pool(pool_count) if use_pool else nullcontext() as pool:
                    
                global_current_time = time.time()

                while True:

                    for inst in self.instances:
                        bf = None if self.best_fish is None else self.best_fish.clone()
                        inst.configure(self.best_brain.clone(), bf, self.generation+1)

                    start_time = time.time()
                    
                    if use_pool:
                        results_async = [pool.apply_async(self.executar_metodo_instancia, (instancia,)) for instancia in self.instances]
                        results = [result.get() for result in results_async]
                    else:
                        results = [self.executar_metodo_instancia(instancia) for instancia in self.instances]

                    bd = 0 if self.best_fish is None else self.best_fish.distance
                    used_mutation_rate = Util.get_mutation_rate(self.generation+1, bd, self.config.training.distance_limit)
                    print(f'Used mutation rate: {used_mutation_rate}, inputs: generation: {self.generation+1}, distance: {bd}, limit: {self.config.training.distance_limit}')

                    results.sort(key=lambda x: x.reward.total, reverse=True)
                    best_fish = results[0]
                    self.best_brain = best_fish.brain
                    self.best_fish = best_fish
                    self.generation += 1
                    elapsed_time = time.time() - start_time

                    self.game_data.brain = best_fish.brain
                    self.game_data.generation = self.generation
                    self.game_data.save()

                    global_elapsed_time = time.time() - global_current_time
                    hours, remainder = divmod(global_elapsed_time, 3600)
                    minutes, seconds = divmod(remainder, 60)


                    print(f'{hours:02.0f}:{minutes:02.0f}:{seconds:02.0f} - End of generation {self.generation}, reward: {best_fish.reward.total:.2f}, dist: {best_fish.distance:.2f} in {elapsed_time:.2f} seconds, mutation rate: {used_mutation_rate:.4f}')

                    if best_fish.distance >= self.config.training.distance_limit:
                        print(f'Best fish got {best_fish.distance:.2f} in generation {self.generation} overcoming the distance limit {self.config.training.distance_limit:.2f} !')

                        if self.config.training.stop_on_reach_distance_limit:
                            print(f'Stop training due to reaching the distance limit!')
                            break
