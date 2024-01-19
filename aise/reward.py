class Reward():
    def __init__(self, entity):
        self.entity = entity
        self.previous_angles = []
        self.total = 0
        self.last_distance = entity.distance

    def update(self):

        self.in_circle()

        self.distance()

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


    def is_moving_in_circles(self):

        if len(self.previous_angles) < 10:
            return False

        total_change = 0
        for i in range(1, len(self.previous_angles)):
            angle_diff = abs(self.previous_angles[i] - self.previous_angles[i - 1])
            total_change += angle_diff

        return total_change > 250

