import numpy as np
from game_context import GameContext

from utils import Direction

class DataObject():
    pass

PENALTY_IN_CIRCLE = -30
PENALTY_COLLISION = -50
PENALTY_UNIQUE_DIRECTION = -10
BONUS_UNIQUE_DIRECTION = 100
DISTANCE_UNIQUE_DIRECTION_LIMIT = 1000
BONUS_DISTANCE_FACTOR = 0.1
BONUS_AREA_EXPLORATION_FACTOR = 0.1
DATA_HISTORY_SIZE = 10

class RewardDataInput():
    def __init__(self, angle, distance_to_wall, direction, speed_up, slow_down, running_distance, speed, center_x, center_y):
        self.angle = angle
        self.distance_to_wall = distance_to_wall
        self.direction = direction
        self.speed_up = speed_up
        self.slow_down = slow_down
        self.running_distance = running_distance
        self.speed = speed
        self.center_x = center_x
        self.center_y = center_y

class DistanceReward():
    def __init__(self):
        self.last_distance = 0

    def calculate(self, hist: list[RewardDataInput]) -> float:
        data = hist[-1]
        points = (data.running_distance - self.last_distance) * BONUS_DISTANCE_FACTOR
        self.last_distance = data.running_distance
        return points
    
class AreaExplorationReward():
    def __init__(self, game_context: GameContext):
        self.last_count = 0
        self.area = np.zeros((game_context.map.map_height, game_context.map.map_width))

    def calculate(self, hist: list[RewardDataInput]) -> float:
        data = hist[-1]

        x = int(data.center_x - 10)
        y = int(data.center_y - 10)
        x2 = int(data.center_x + 10)
        y2 = int(data.center_y + 10)

        self.area[y:y2, x:x2] = 1

        ones_count = np.count_nonzero(self.area)
        points = (ones_count - self.last_count) * BONUS_AREA_EXPLORATION_FACTOR
        self.last_count = ones_count
        return points    

class InCircleReward():
    def __init__(self):
        self.last_angle = None
        self.accumulated_rotation = 0

    def calculate(self, hist: list[RewardDataInput]) -> float:
        data = hist[-1]

        if self.last_angle is None:
            self.last_angle = data.angle

        if data.direction == Direction.RIGHT:
            if self.last_angle <= data.angle:
                angle_change = data.angle - self.last_angle
            else:
                angle_change = 360 - self.last_angle + data.angle
        
        if data.direction == Direction.LEFT:
            if self.last_angle >= data.angle:
                angle_change = data.angle - self.last_angle
            else:
                angle_change = data.angle + self.last_angle - 360

        if data.direction == Direction.STRAIGHT:
            angle_change = 0

        self.accumulated_rotation += angle_change
        self.last_angle = data.angle

        if len(hist) > 3:
            if data.direction == hist[-1].direction == hist[-2].direction != hist[-3].direction:
                self.accumulated_rotation = 0

        if abs(self.accumulated_rotation) >= 360:
            return PENALTY_IN_CIRCLE
        
        return 0


class UniqueDirectionReward():
    def __init__(self):
        self.direction_accumulated_distance = 0
        self.moved_straight = False
        self.moved_right = False
        self.moved_left = False

    def calculate(self, hist: list[RewardDataInput]) -> float:

        points = 0

        data = hist[-1]

        self.direction_accumulated_distance += data.speed

        if data.direction == Direction.LEFT:
            self.moved_left = True
        elif data.direction == Direction.RIGHT:
            self.moved_right = True
        elif data.direction == Direction.STRAIGHT:
            self.moved_straight = True

            
        if self.direction_accumulated_distance > DISTANCE_UNIQUE_DIRECTION_LIMIT:

            if not self.moved_straight or not self.moved_left or not self.moved_right:
                points = PENALTY_UNIQUE_DIRECTION
            else:
                points = BONUS_UNIQUE_DIRECTION

            self.direction_accumulated_distance = 0
            self.moved_straight = False
            self.moved_right = False
            self.moved_left = False

        return points


class CollisionReward():
    def __init__(self):
        pass

    def calculate(self, hist: list[RewardDataInput]) -> float:
        data = hist[-1]
        
        if data.distance_to_wall <= 10:
            return PENALTY_COLLISION

        return 0



class Reward():
    def __init__(self, game_context: GameContext):
        #reward
        self.total = 0
        self.game_context = game_context

        self.distance_reward = DistanceReward()
        self.in_circle_reward = InCircleReward()
        self.unique_direction_reward = UniqueDirectionReward()
        self.collision_reward = CollisionReward()
        self.area_exploration_reward = AreaExplorationReward(game_context)
        self.data_history: list[RewardDataInput] = []

    def update(self, data: RewardDataInput):
        
        self.data_history.append(data)
        if len(self.data_history) > DATA_HISTORY_SIZE:
            self.data_history = self.data_history[1:]

        self.total += self.distance_reward.calculate(self.data_history)
        self.total += self.in_circle_reward.calculate(self.data_history)
        self.total += self.unique_direction_reward.calculate(self.data_history)
        self.total += self.collision_reward.calculate(self.data_history)
        self.total += self.area_exploration_reward.calculate(self.data_history)
