import numpy as np

from aise.utils import Direction

class DataObject():
    pass

PENALTY_IN_CIRCLE = 30
PENALTY_UNIQUE_DIRECTION = 5
BONUS_DISTANCE_FACTOR = 0.1
DATA_HISTORY_SIZE = 30

class Reward():
    def __init__(self):
        self.total = 0
        self.last_angle = None
        self.accumulated_rotation = 0
        self.last_distance = 0
        self.data_history = []

    def update(self, id, angle, distance_to_wall, direction, speed_up, slow_down, running_distance, speed, center_x, center_y):
        
        data = DataObject()
        data.angle = angle
        data.distance_to_wall = distance_to_wall
        data.direction = direction
        data.speed_up = speed_up
        data.slow_down = slow_down
        data.running_distance = running_distance
        data.speed = speed
        data.center_x = center_x
        data.center_y = center_y

        self.data_history.append(data)

        if len(self.data_history) > DATA_HISTORY_SIZE:
            self.data_history = self.data_history[1:]

        self.update_distance(data)

        self.update_in_circle(data)

        if self.is_in_cicle():
            self.total -= PENALTY_IN_CIRCLE

        self.update_unique_direction()



    def update_unique_direction(self):
        #Check if entity used all directions in last data history

        found_straight = False
        found_right = False
        found_left = False

        if len(self.data_history) < DATA_HISTORY_SIZE:
            return False

        for d in self.data_history:
            if d.direction == Direction.LEFT:
                found_left = True
            elif d.direction == Direction.RIGHT:
                found_right = True
            elif d.direction == Direction.STRAIGHT:
                found_straight = True
            
        if not found_left or not found_right or not found_straight:
            self.total -= PENALTY_UNIQUE_DIRECTION
            return True

        return False

    def update_distance(self, data):
        self.total += (data.running_distance - self.last_distance) * BONUS_DISTANCE_FACTOR
        self.last_distance = data.running_distance

    def update_in_circle(self, data):

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

        if len(self.data_history) > 3:
            if data.direction == self.data_history[-1].direction == self.data_history[-2].direction != self.data_history[-3].direction:
                self.accumulated_rotation = 0

    def is_in_cicle(self):
        return abs(self.accumulated_rotation) >= 360
    