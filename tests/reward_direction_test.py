import unittest
from aise.utils import Direction
from aise.reward import Reward, DATA_HISTORY_SIZE

class TestReward(unittest.TestCase):


    def test_direction_history_size_less(self):
        data = []
        last_angle = 0
        last_dist = 0

        #50 ciclos em linha reta
        for i in range(0, DATA_HISTORY_SIZE-1):
            last_angle -= 0
            last_angle = last_angle % 360
            last_dist += 1
            data +=  [last_angle, 90, Direction.STRAIGHT, False, False, last_dist, 1, 0, 0],

        reward = Reward()

        for i in range(len(data)):
            d = data[i] 
            reward.update(0, d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8])
            self.assertEqual(reward.update_unique_direction(), False)


    def test_direction_no_change(self):
        data = []
        last_angle = 0
        last_dist = 0

        #50 ciclos em linha reta
        for i in range(0, DATA_HISTORY_SIZE+5):
            last_angle -= 0
            last_angle = last_angle % 360
            last_dist += 1
            data +=  [last_angle, 90, Direction.STRAIGHT, False, False, last_dist, 1, 0, 0],

        reward = Reward()

        for i in range(len(data)):
            d = data[i] 
            reward.update(0, d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8])

        self.assertEqual(reward.update_unique_direction(), True)


    def test_direction_parcial_change(self):
        data = []
        last_angle = 0
        last_dist = 0

        #50 ciclos em linha reta
        for i in range(0, DATA_HISTORY_SIZE+5):
            last_angle -= 0
            last_angle = last_angle % 360
            last_dist += 1
            data +=  [last_angle, 90, Direction.STRAIGHT, False, False, last_dist, 1, 0, 0],

        for i in range(0, 5):
            last_angle -= 5
            last_angle = last_angle % 360
            last_dist += 1
            data +=  [last_angle, 90, Direction.LEFT, False, False, last_dist, 1, 0, 0],
        
        reward = Reward()

        for i in range(len(data)):
            d = data[i] 
            reward.update(0, d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8])

        self.assertEqual(reward.update_unique_direction(), True)


    def test_direction_sucess_change(self):
        data = []
        last_angle = 0
        last_dist = 0

        #50 ciclos em linha reta
        for i in range(0, DATA_HISTORY_SIZE+5):
            last_angle -= 0
            last_angle = last_angle % 360
            last_dist += 1
            data +=  [last_angle, 90, Direction.STRAIGHT, False, False, last_dist, 1, 0, 0],

        for i in range(0, 5):
            last_angle -= 5
            last_angle = last_angle % 360
            last_dist += 1
            data +=  [last_angle, 90, Direction.LEFT, False, False, last_dist, 1, 0, 0],
        
        for i in range(0, 5):
            last_angle -= 5
            last_angle = last_angle % 360
            last_dist += 1
            data +=  [last_angle, 90, Direction.RIGHT, False, False, last_dist, 1, 0, 0],
        
        reward = Reward()

        for i in range(len(data)):
            d = data[i] 
            reward.update(0, d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8])

        self.assertEqual(reward.update_unique_direction(), False)


if __name__ == '__main__':
    unittest.main()