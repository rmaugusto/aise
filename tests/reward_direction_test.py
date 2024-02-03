import unittest
from aise.utils import Direction
from aise.reward import DATA_HISTORY_SIZE, DISTANCE_UNIQUE_DIRECTION_LIMIT, PENALTY_UNIQUE_DIRECTION, RewardDataInput, UniqueDirectionReward

class TestReward(unittest.TestCase):


    def test_direction_less_limit(self):
        data_history:list[RewardDataInput] = []
        last_angle = 100
        last_dist = 0

        reward = UniqueDirectionReward()

        #Gira 400 graus para direita
        for i in range(0, DISTANCE_UNIQUE_DIRECTION_LIMIT):
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

    def test_direction_just_left(self):
        data_history:list[RewardDataInput] = []
        last_angle = 100
        last_dist = 0

        reward = UniqueDirectionReward()

        #Gira 400 graus para direita
        for i in range(0, DISTANCE_UNIQUE_DIRECTION_LIMIT+1):
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

        self.assertEqual(points, PENALTY_UNIQUE_DIRECTION)


    def test_direction_just_right(self):
        data_history:list[RewardDataInput] = []
        last_angle = 100
        last_dist = 0

        reward = UniqueDirectionReward()

        #Gira 400 graus para direita
        for i in range(0, DISTANCE_UNIQUE_DIRECTION_LIMIT+1):
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
            
        self.assertEqual(points, PENALTY_UNIQUE_DIRECTION)


    def test_direction_left_right(self):
        data_history:list[RewardDataInput] = []
        last_angle = 100
        last_dist = 0

        reward = UniqueDirectionReward()

        for i in range(0, int(DISTANCE_UNIQUE_DIRECTION_LIMIT/2)):
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
            
        for i in range(0, int(DISTANCE_UNIQUE_DIRECTION_LIMIT/2)+1):
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


        self.assertEqual(points, PENALTY_UNIQUE_DIRECTION)


    def test_direction_all(self):
        data_history:list[RewardDataInput] = []
        last_angle = 100
        last_dist = 0

        reward = UniqueDirectionReward()

        for i in range(0, int(DISTANCE_UNIQUE_DIRECTION_LIMIT/3)):
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
            
        for i in range(0, int(DISTANCE_UNIQUE_DIRECTION_LIMIT/3)):
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


        for i in range(0, int(DISTANCE_UNIQUE_DIRECTION_LIMIT/3)+1):
            last_angle -= 0
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

if __name__ == '__main__':
    unittest.main()