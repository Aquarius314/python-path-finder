import numpy as np
import random
from wall import Wall


class World:

    RANDOM_OBSTACLES = True
    RANDOM_WALLS = True
    UNREACHABLE = False  # it will be impossible for sure to find an exit!

    OBSTACLES_PERCENTAGE = 40
    WALLS = 1500
    walls = []

    # optimization stuff
    display_fields_once = True
    clearing = True

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._fields = np.zeros((width, height))
        if self.RANDOM_OBSTACLES:
            self._generate_random_obstacles()
        if self.RANDOM_WALLS:
            self._generate_maze()
        self._set_goal()
        self._set_start_position()

    def _generate_maze(self):
        self._add_wall(self._fields, int(self.width/3), int(self.height/3), int(self.width/3), 2)
        self._add_wall(self._fields, 2*int(self.width/3), int(self.height/3), 2, int(self.height/3))
        # self._add_wall(self._fields, 70, 70, 20, 2)
        # self._add_wall(self._fields, 20, 20, 2, 90)
        # self._add_wall(self._fields, 40, 0, 2, 90)
        # self._add_wall(self._fields, 60, 20, 2, 90)
        # self._add_wall(self._fields, 10, 30, 25, 2)
        # self._add_wall(self._fields, 30, 50, 25, 2)
        # self._add_wall(self._fields, 50, 70, 25, 2)
        # self._add_wall(self._fields, 3, 7, 12, 2)
        # self._add_wall(self._fields, 3, 7, 2, 4)

        # self._add_wall(self._fields, int(self.width/2-100), int(self.height/2-100), 200, 200)

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
        self.walls.append(Wall(x, y, width, height))
        for a in range(x, x+width):
            for b in range(y, y+height):
                if 0 <= a < self.width and 0 <= b < self.height:
                    array[a, b] = 1

    def _set_start_position(self):
        self.start_x = 8
        self.start_y = int(self.height - 3)
        for a in range(-2, 3):
            for b in range(-2, 3):
                self._fields[self.start_x+a, self.start_y+b] = 0

    def _set_goal(self):
        self.goal_x = int(self.width-8)
        self.goal_y = 3
        for a in range(-2, 3):
            for b in range(-2, 3):
                self._fields[self.goal_x+a, self.goal_y+b] = 0

    def _set_random_goal(self):
        if self.UNREACHABLE:
            self.goal_x = -2
            self.goal_y = -2
        else:
            self.goal_x = random.randint(2, self.width-3)
            self.goal_y = random.randint(2, self.height-3)
            for a in range(-2, 3):
                for b in range(-2, 3):
                    self._fields[self.goal_x+a, self.goal_y+b] = 0

    def _generate_random_obstacles(self):
        for x in range(self.width):
            for y in range(self.height):
                if random.randint(1, 100) <= self.OBSTACLES_PERCENTAGE:
                    self._fields[x, y] = 1
                    self.walls.append(Wall(x, y, 1, 1))

    def get_goal_position(self):
        return self.goal_x, self.goal_y

    def get_start_position(self):
        return self.start_x, self.start_y

    def get_fields(self):
        return self._fields

    def get_field_value(self, x, y):
        return self._fields[x, y]

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_size(self):
        return self.width, self.height

    def display(self, gui):
        if self.clearing:
            gui.clear()
            gui.display_fields(self.walls, self.get_width(), self.get_height())
        else:
            if self.display_fields_once:
                gui.display_fields(self.walls, self.get_width(), self.get_height())
                self.display_fields_once = False
        gui.display_start(self.get_start_position())
        gui.display_goal(self.get_goal_position())
