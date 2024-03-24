from enum import Enum
import math
from queue import Queue
from threading import Thread


class Direction(Enum):
    STRAIGHT = 1
    LEFT = 2
    RIGHT = 3

class Util:
    #static method
    @staticmethod
    def get_mutation_rate(epoch_number, travelled_distance, distance_limit):
        minimum_rate = 0.01  # Minimum mutation rate
        threshold_distance = 1000  # Distance below which full mutation is applied
        scaled_rate = (travelled_distance / distance_limit) * 0.5  # Scaling factor of 0.5
        decayed_rate = scaled_rate * 0.95 ** epoch_number  # Decay
        sigmoid_rate = 1 / (1 + math.exp(-(travelled_distance - threshold_distance) / 1000))  # Sigmoid transition
        no_mutation_prob = min(1, decayed_rate * sigmoid_rate)  # Probability of **not** mutating
        return 1 - no_mutation_prob  # Return mutation rate

    
class Worker(Thread):
    """Thread executing tasks from a given tasks queue"""
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try:
                func(*args, **kargs)
            except:
                pass
            finally:
                self.tasks.task_done()


class ThreadPool:
    """Pool of threads consuming tasks from a queue"""
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads):
            Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        """Add a task to the queue"""
        self.tasks.put((func, args, kargs))

    def wait_completion(self):
        """Wait for completion of all the tasks in the queue"""
        self.tasks.join()
