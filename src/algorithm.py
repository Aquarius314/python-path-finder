from gui import Gui
from world import World
import pygame
import time
import numpy as np


class Algorithm:

    # WAVE PROPAGATION ALGORITHM
    # -1: obstacle, -2: goal, any other: number of steps to get there (counting start as 1)

    MAX_ITERATIONS = 100000
    TILE_SIZE = 5
    delay = 0.0
    path = []

    steps = []

    ENABLE_CORNER_NEIGHBOURS = False

    # tmp
    RED = 255
    GREEN = 0
    BLUE = 1
    COLOR_ITERATIONS = 0

    goal_reached = False
    last_steps = []
    current_iteration_steps = []

    def __init__(self, width, height, screen):
        self.width = width
        self.height = height
        self.gui = Gui(width, height, screen)
        self.WORLD_WIDTH = int(width / self.TILE_SIZE)
        self.WORLD_HEIGHT = int(height / self.TILE_SIZE)
        print("World dimensions set to", self.WORLD_WIDTH, self.WORLD_HEIGHT)
        self.world = World(self.WORLD_WIDTH, self.WORLD_HEIGHT)
        self.iterations = 0
        self.setup()

    def setup(self):
        self.rewrite_world_to_steps_array()

    def rewrite_world_to_steps_array(self):
        self.steps = np.zeros((self.WORLD_WIDTH, self.WORLD_HEIGHT))
        for y in range(self.WORLD_WIDTH):
            for x in range(self.WORLD_HEIGHT):
                if self.world.get_field_value(x, y) == 1:
                    self.steps[x, y] = -1
        # rewrite start and goal positions
        start_x, start_y = self.world.get_start_position()
        self.steps[start_x, start_y] = 1
        self.last_steps.append((start_x, start_y))
        goal_x, goal_y = self.world.get_goal_position()
        self.steps[goal_x, goal_y] = -2

    def run(self):
        self.iterations += 1
        # if self.iterations%1 == 0:
        #     print("running iteration nr", self.iterations)
        if self.iterations >= self.MAX_ITERATIONS:
            return False

        # algo guts here
        self.calculate()

        self.update_gui()
        if self.delay != 0:
            time.sleep(self.delay)
        return True

    def calculate(self):
        if self.goal_reached:
            self.reverse_path()
        else:
            # mark neighbour fields with distance+1
            for step in self.last_steps:
                self._propagate_step(step)
            self.last_steps = self.current_iteration_steps[:]
            self.current_iteration_steps.clear()

    def reverse_path(self):
        self.gui.clear()
        self.last_steps.clear()
        position = self.world.get_goal_position()
        while True:
            new_position = self.get_smaller_neighbour(position)
            self.last_steps.append(new_position)
            x, y = new_position
            start_x, start_y = self.world.get_start_position()
            if x == start_x and y == start_y:
                break
            position = new_position

    def get_smallest_neighbour(self, position):
        x, y = position
        smallest_position = x, y
        smallest = 1000
        for a in range(x-1, x+2):
            for b in range(y-1, y+2):
                if (a != x or b != y) and 0 <= a < len(self.steps) and 0 <= b < len(self.steps[0]):
                    if 0 < self.steps[a, b] < smallest:
                        smallest = self.steps[a, b]
                        smallest_position = a, b
        return smallest_position

    def find_differenced_neighbour(self, difference, current_value, position):
        x, y = position
        for a in range(x-1, x+2):
            for b in range(y-1, y+2):
                if (a != x or b != y) and 0 <= a < len(self.steps) and 0 <= b < len(self.steps[0]):
                    neighbour_value = self.steps[a, b]
                    if neighbour_value + difference == current_value:
                        return a, b
        return -1, -1

    def get_smaller_neighbour(self, position):
        x, y = position
        current_value = self.steps[x, y]

        a, b = self.find_differenced_neighbour(2, current_value, (x, y))
        if a != -1:
            return a, b
        a, b = self.find_differenced_neighbour(1, current_value, (x, y))
        return a, b

    def _propagate_step(self, step):
        x, y = step
        distance = self.steps[x, y]
        # cross-style (up, down, left, right)
        self._check_field(x+1, y, distance)
        self._check_field(x-1, y, distance)
        self._check_field(x, y+1, distance)
        self._check_field(x, y-1, distance)
        if self.ENABLE_CORNER_NEIGHBOURS:
            self._check_field(x+1, y+1, distance)
            self._check_field(x-1, y+1, distance)
            self._check_field(x+1, y-1, distance)
            self._check_field(x-1, y-1, distance)

    def _check_field(self, x, y, distance):
        if 0 <= x < len(self.steps) and 0 <= y < len(self.steps[0]):
            if self.steps[x, y] == 0:
                self.steps[x, y] = distance + 1
                self.current_iteration_steps.append((x, y))
            elif self.steps[x, y] == -2:
                self.steps[x, y] = distance + 1
                self.goal_reached = True

    def update_gui(self):
        self.gui.clear()
        self.gui.display_fields(self.world.get_fields(), self.TILE_SIZE, self.WORLD_WIDTH, self.WORLD_HEIGHT)
        self.gui.display_start(self.world.get_start_position(), self.TILE_SIZE)
        self.gui.display_goal(self.world.get_goal_position(), self.TILE_SIZE)
        self.display_last_steps()
        # self.display_all_steps()

    def _switch_colors(self, mode):
        if mode == 0:
            self.BLUE += 1
        elif mode == 1:
            self.RED -= 1
        elif mode == 2:
            self.GREEN += 1
        elif mode == 3:
            self.BLUE -= 1
        elif mode == 4:
            self.RED += 1
        elif mode == 5:
            self.GREEN -= 1

    def display_last_steps(self):

        self.COLOR_ITERATIONS += 1
        color_mode = int((self.COLOR_ITERATIONS/255)) % 6
        self._switch_colors(color_mode)

        color = int(self.RED), int(self.GREEN), int(self.BLUE)
        print(color)
        for step in self.last_steps:
            x, y = step
            self.gui.display_step((x, y), self.TILE_SIZE, color)

    def display_all_steps(self):
        for y in range(len(self.steps)):
            line = ""
            for x in range(len(self.steps[0])):
                if self.steps[x, y] == -1:
                    line += "  *"
                else:
                    if 10 > self.steps[x, y] > -2:
                        line += " "
                    line += " " + str(int(self.steps[x, y]))
            print(line)
