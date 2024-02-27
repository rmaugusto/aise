from aise import AiseTrainer
import time
import multiprocessing

from game_context import GameData
from neural_network_pytorch import NeuralNetworkPyTorch

class TrainingHeadless():
    def __init__(self, config):
        self.instances = []
        self.threads = []
        self.update_time = time.time()
        self.config = config
        self.game_data = GameData()
        self.generation = 0
        self.best_brain = None

    def setup(self):

        try:        
            gd = GameData.load()
            #self.generation = gd.generation
            self.best_brain = gd.brain
        except:

            size_input = 1 + 1 + 1 + 1 + self.config.training.sensor_count
            size_hidden = 6
            size_output = 4

            self.best_brain = NeuralNetworkPyTorch([size_input, size_hidden, size_hidden, size_output],'relu')


        for i in range(self.config.training.instances):
            inst = AiseTrainer( self.config.clone() )
            inst.load()

            self.instances.append(inst)


    def executar_metodo_instancia(self, instancia):
        return instancia.run_until_done()

    def run(self):


        while True:

            for inst in self.instances:
                inst.configure(self.best_brain.clone())

            pool_count = None if self.config.training.pool_size == -1 else self.config.training.pool_size

            with multiprocessing.Pool(pool_count) as pool:

                start_time = time.time()
                results_async = [pool.apply_async(self.executar_metodo_instancia, (instancia,)) for instancia in self.instances]
                results = [result.get() for result in results_async]
                results.sort(key=lambda x: x.reward.total, reverse=True)
                best_fish = results[0]
                self.best_brain = best_fish.brain
                self.generation += 1
                elapsed_time = time.time() - start_time

                print(f'End of generation {self.generation}, reward: {best_fish.reward.total}, dist: {best_fish.distance} in {elapsed_time:.2f} seconds')


        # while True:
        #     self.counter += 1
        #     self.on_update( 1 / self.counter)

        #     if time.time() - self.update_time >= 1:
        #         self.on_draw()
        #         self.counter = 0
        #         self.update_time = time.time()

