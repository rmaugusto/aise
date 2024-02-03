import unittest
from aise.utils import Direction
from aise.reward import DATA_HISTORY_SIZE, PENALTY_IN_CIRCLE, InCircleReward, Reward, RewardDataInput

class TestReward(unittest.TestCase):

    def test_run_circle_left_short(self):

        data_history:list[RewardDataInput] = []
        last_angle = 100
        last_dist = 0


        reward = InCircleReward()

        #Gira 400 graus para direita
        for i in range(0, 22):
            last_angle -= 5
            last_angle = last_angle % 360
            last_dist += 8.5
            data_history.append(
                    RewardDataInput(angle=last_angle, distance_to_wall=100, direction=Direction.LEFT, \
                                speed_up=False, slow_down=False, running_distance=last_dist, speed=1, center_x=0, center_y=0)
                )
            if len(data_history) > DATA_HISTORY_SIZE:
                data_history = data_history[1:]

            points = reward.calculate(data_history)
            self.assertEqual(points, 0)

    def test_run_circle_complete_right(self):

        data_history:list[RewardDataInput] = []
        last_angle = 100
        last_dist = 0


        reward = InCircleReward()

        #Gira 400 graus para direita
        for i in range(0, 80):
            last_angle += 5
            last_angle = last_angle % 360
            last_dist += 1
            data_history.append(
                    RewardDataInput(angle=last_angle, distance_to_wall=100, direction=Direction.RIGHT, \
                                speed_up=False, slow_down=False, running_distance=last_dist, speed=1, center_x=0, center_y=0)
                )
            if len(data_history) > DATA_HISTORY_SIZE:
                data_history = data_history[1:]

            points = reward.calculate(data_history)

            if i < 72:
                self.assertEqual(points, 0)
            else:
                self.assertEqual(points, PENALTY_IN_CIRCLE)

    def test_run_circle_complete_left(self):
        data_history:list[RewardDataInput] = []
        last_angle = 100
        last_dist = 0


        reward = InCircleReward()

        #Gira 400 graus para direita
        for i in range(0, 80):
            last_angle -= 5
            last_angle = last_angle % 360
            last_dist += 1
            data_history.append(
                    RewardDataInput(angle=last_angle, distance_to_wall=100, direction=Direction.LEFT, \
                                speed_up=False, slow_down=False, running_distance=last_dist, speed=1, center_x=0, center_y=0)
                )
            if len(data_history) > DATA_HISTORY_SIZE:
                data_history = data_history[1:]

            points = reward.calculate(data_history)

            if i < 72:
                self.assertEqual(points, 0)
            else:
                self.assertEqual(points, PENALTY_IN_CIRCLE)



    def test_run_circle_incomplete_and_walk(self):


        data_history:list[RewardDataInput] = []
        last_angle = 100
        last_dist = 0


        reward = InCircleReward()

        #Gira 300 graus para direita
        for i in range(0, 59):
            last_angle += 5
            last_angle = last_angle % 360
            last_dist += 1
            data_history.append(
                    RewardDataInput(angle=last_angle, distance_to_wall=100, direction=Direction.RIGHT, \
                                speed_up=False, slow_down=False, running_distance=last_dist, speed=1, center_x=0, center_y=0)
                )
            if len(data_history) > DATA_HISTORY_SIZE:
                data_history = data_history[1:]

            points = reward.calculate(data_history)

            self.assertEqual(points, 0)

        #Gira 5 linha reta
        for i in range(0, 4):
            last_angle += 0
            last_angle = last_angle % 360
            last_dist += 1
            data_history.append(
                    RewardDataInput(angle=last_angle, distance_to_wall=100, direction=Direction.STRAIGHT, \
                                speed_up=False, slow_down=False, running_distance=last_dist, speed=1, center_x=0, center_y=0)
                )
            if len(data_history) > DATA_HISTORY_SIZE:
                data_history = data_history[1:]

            points = reward.calculate(data_history)

            self.assertEqual(points, 0)

        #Gira 300 graus para esquerda
        for i in range(0, 59):
            last_angle -= 5
            last_angle = last_angle % 360
            last_dist += 1
            data_history.append(
                    RewardDataInput(angle=last_angle, distance_to_wall=100, direction=Direction.LEFT, \
                                speed_up=False, slow_down=False, running_distance=last_dist, speed=1, center_x=0, center_y=0)
                )
            if len(data_history) > DATA_HISTORY_SIZE:
                data_history = data_history[1:]

            points = reward.calculate(data_history)

            self.assertEqual(points, 0)



    def test_run_circle_right_incomplete_and_left(self):

        data_history:list[RewardDataInput] = []
        last_angle = 100
        last_dist = 0

        reward = InCircleReward()

        #Gira 300 graus para direita
        for i in range(0, 59):
            last_angle += 5
            last_angle = last_angle % 360
            last_dist += 1
            data_history.append(
                    RewardDataInput(angle=last_angle, distance_to_wall=100, direction=Direction.RIGHT, \
                                speed_up=False, slow_down=False, running_distance=last_dist, speed=1, center_x=0, center_y=0)
                )
            if len(data_history) > DATA_HISTORY_SIZE:
                data_history = data_history[1:]

            points = reward.calculate(data_history)

            self.assertEqual(points, 0)

        #Gira 5 graus para esquerda
        for i in range(0, 4):
            last_angle -= 5
            last_angle = last_angle % 360
            last_dist += 1
            data_history.append(
                    RewardDataInput(angle=last_angle, distance_to_wall=100, direction=Direction.LEFT, \
                                speed_up=False, slow_down=False, running_distance=last_dist, speed=1, center_x=0, center_y=0)
                )
            if len(data_history) > DATA_HISTORY_SIZE:
                data_history = data_history[1:]

            points = reward.calculate(data_history)

            self.assertEqual(points, 0)

        #Gira 300 graus para esquerda
        for i in range(0, 59):
            last_angle += 5
            last_angle = last_angle % 360
            last_dist += 1
            data_history.append(
                    RewardDataInput(angle=last_angle, distance_to_wall=100, direction=Direction.RIGHT, \
                                speed_up=False, slow_down=False, running_distance=last_dist, speed=1, center_x=0, center_y=0)
                )
            if len(data_history) > DATA_HISTORY_SIZE:
                data_history = data_history[1:]

            points = reward.calculate(data_history)

            self.assertEqual(points, 0)





if __name__ == '__main__':
    unittest.main()