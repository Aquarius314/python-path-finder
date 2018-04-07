import numpy as np
import random


class World:

    RANDOM_OBSTACLES = True
    RANDOM_WALLS = False
    UNREACHABLE = True  # it will be impossible for sure to find an exit!

    OBSTACLES_PERCENTAGE = 40
    WALLS = 200

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._fields = np.zeros((width, height))
        if self.RANDOM_OBSTACLES:
            self._generate_random_obstacles()
        if self.RANDOM_WALLS:
            self._generate_maze()
        self._set_random_goal()
        self._set_start_position()

    def _generate_maze(self):
        for i in range(self.WALLS):
            self._add_random_wall(self._fields)

    def _add_random_wall(self, array):
        length = random.randint(10, 20)
        orientation = random.randint(0, 1)
        thickness = random.randint(1, 4)
        x, y = random.randint(0, self.width-length-thickness), random.randint(0, self.width-length-thickness)
        if orientation == 0:
            self._add_wall(array, x, y, length, thickness)
        else:
            self._add_wall(array, x, y, thickness, length)

    def _add_wall(self, array, x, y, width, height):
        for a in range(x, x+width):
            for b in range(y, y+height):
                array[a, b] = 1

    def _set_start_position(self):
        self.start_x = int(self.width/2)
        self.start_y = int(self.height/2)
        self._fields[self.start_x, self.start_y] = 0

    def _set_random_goal(self):
        if self.UNREACHABLE:
            self.goal_x = -2
            self.goal_y = -2
        else:
            self.goal_x = random.randint(0, self.width-1)
            self.goal_y = random.randint(0, self.height-1)

    def _generate_random_obstacles(self):
        for x in range(self.width):
            for y in range(self.height):
                if random.randint(1, 100) <= self.OBSTACLES_PERCENTAGE:
                    self._fields[x, y] = 1

    def get_goal_position(self):
        return self.goal_x, self.goal_y

    def get_start_position(self):
        return self.start_x, self.start_y

    def get_fields(self):
        return self._fields

    def get_field_value(self, x, y):
        return self._fields[x, y]
