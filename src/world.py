import numpy as np
import random


class World:

    OBSTACLES_PERCENTAGE = 20

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._fields = np.zeros((width, height))
        self._generate_random_obstacles()
        self._set_random_goal()
        self._set_start_position()

    def _set_start_position(self):
        self.start_x = 1
        self.start_y = 1
        self._fields[self.start_x, self.start_y] = 0

    def _set_random_goal(self):
        self.goal_x = random.randint(0, self.width-1)
        self.goal_y = random.randint(0, self.height-1)

    def _generate_random_obstacles(self):
        for x in range(self.width):
            for y in range(self.height):
                if random.randint(0, 100) <= self.OBSTACLES_PERCENTAGE:
                    self._fields[x, y] = 1

    def get_goal_position(self):
        return self.goal_x, self.goal_y

    def get_start_position(self):
        return self.start_x, self.start_y

    def get_fields(self):
        return self._fields
