import numpy as np


class Reward():
    def __init__(self, entity):
        self.entity = entity
        self.previous_angles = []
        self.min_distances = np.array([])
        self.total = 0
        self.last_distance = entity.distance

    def update(self):


        self.distance()

        self.in_circle()

        
        #if self.is_moving_away_from_wall() > 0:
        #    self.total += 40

    def is_moving_away_from_wall(self):

        self.min_distances = np.append(self.min_distances, self.entity.sensor.min_distance)

        if len(self.min_distances) > 20:
            self.min_distances = self.min_distances[1:]
        else:
            return -1

        slopes = np.diff(self.min_distances)
        average_slope = np.mean(slopes)

        #print(self.min_distances.shape, average_slope)
        return average_slope

    def distance(self):

        if (self.entity.distance - self.last_distance) >= 100:
            self.last_distance = self.entity.distance
            self.total += 10

    def in_circle(self):
        self.previous_angles.append(self.entity.angle)

        if len(self.previous_angles) > 10:
            self.previous_angles.pop(0)

        if self.is_moving_in_circles():
            self.total -= 20
            return True
        
        return False


    def is_moving_in_circles(self):

        if len(self.previous_angles) < 10:
            return False

        total_change = 0
        for i in range(1, len(self.previous_angles)):
            angle_diff = abs(self.previous_angles[i] - self.previous_angles[i - 1])
            total_change += angle_diff

        return total_change > 360

