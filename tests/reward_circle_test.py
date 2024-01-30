import unittest
from aise.utils import Direction
from aise.reward import Reward

class TestReward(unittest.TestCase):

    def test_run_circle_left_short(self):
        data = []
        last_angle = 100
        last_dist = 0

        #Gira 400 graus para direita
        for i in range(0, 22):
            last_angle -= 5
            last_angle = last_angle % 360
            last_dist += 8.5
            data +=  [last_angle, 90, Direction.LEFT, False, False, last_dist, 1, 0, 0],

        reward = Reward()

        for i in range(len(data)):
            d = data[i] 
            reward.update(0, d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8])
            #print(d, reward.accumulated_rotation)
            self.assertEqual(reward.is_in_cicle() , False)

    def test_run_circle_complete_right(self):

        data = []
        last_angle = 90
        last_dist = 0

        #Gira 400 graus para direita
        for i in range(0, 80):
            last_angle += 5
            last_angle = last_angle % 360
            last_dist += 1
            data +=  [last_angle, 100, Direction.RIGHT, False, False, last_dist, 1, 0, 0],

        reward = Reward()

        for i in range(len(data)):
            d = data[i]
            reward.update(0, d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8])

            if i < 72:
                self.assertEqual(reward.is_in_cicle() , False)
            else:
                self.assertEqual(reward.is_in_cicle() , True)

    def test_run_circle_complete_left(self):
        data = []
        last_angle = 90
        last_dist = 0

        #Gira 400 graus para esquerda
        for i in range(0, 80):
            last_angle -= 5
            last_angle = last_angle % 360
            last_dist += 1
            data +=  [last_angle, 100, Direction.LEFT, False, False, last_dist, 1, 0, 0],

        reward = Reward()

        for i in range(len(data)):
            d = data[i]
            reward.update(0, d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8])

            if i < 72:
                self.assertEqual(reward.is_in_cicle() , False)
            else:
                self.assertEqual(reward.is_in_cicle() , True)


    def test_run_circle_incomplete_and_walk(self):
        data = []
        last_angle = 90
        last_dist = 0

        #Gira 300 graus para direita
        for i in range(0, 59):
            last_angle += 5
            last_angle = last_angle % 360
            last_dist += 1
            data +=  [last_angle, 100, Direction.RIGHT, False, False, last_dist, 1, 0, 0],

        #Anda 5 em linha reta
        for i in range(0, 4):
            last_dist += 1
            data +=  [last_angle, 100, Direction.STRAIGHT, False, False, last_dist, 1, 0, 0],

        #Gira 300 graus para direita
        for i in range(0, 59):
            last_angle += 5
            last_angle = last_angle % 360
            last_dist += 1
            data +=  [last_angle, 100, Direction.RIGHT, False, False, last_dist, 1, 0, 0],

        reward = Reward()

        for i in range(len(data)):
            d = data[i]
            reward.update(0, d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8])
            self.assertEqual(reward.is_in_cicle() , False)

    def test_run_circle_right_incomplete_and_left(self):
        data = []
        last_angle = 90
        last_dist = 0

        #Gira 300 graus para direita
        for i in range(0, 59):
            last_angle += 5
            last_angle = last_angle % 360
            last_dist += 1
            data +=  [last_angle, 100, Direction.RIGHT, False, False, last_dist, 1, 0, 0],

        #Anda 50 graus para esquerda
        for i in range(0, 9):
            last_dist += 1
            data +=  [last_angle, 100, Direction.LEFT, False, False, last_dist, 1, 0, 0],

        #Gira 300 graus para direita
        for i in range(0, 59):
            last_angle += 5
            last_angle = last_angle % 360
            last_dist += 1
            data +=  [last_angle, 100, Direction.RIGHT, False, False, last_dist, 1, 0, 0],

        reward = Reward()

        for i in range(len(data)):
            d = data[i]
            reward.update(0, d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8])
            self.assertEqual(reward.is_in_cicle() , False)


if __name__ == '__main__':
    unittest.main()