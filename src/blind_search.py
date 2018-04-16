from gui import Gui
from world import World
import pygame
import time
import math
import random


class BlindSearch:

    NAME = "Blind Search"

    MAX_ITERATIONS = 100000
    COST = 0
    TILE_SIZE = 6
    path = []
    checked = []

    freeze = False
    RETURNS = 0
    delay = 0.0
    head = 0, 0
    goal_reached = False

    def __init__(self, width, height, world, gui):
        self.width = width
        self.height = height
        self.world = world
        self.gui = gui
        self.iterations = 0
        self.setup()

    def setup(self):
        self.head = self.world.get_start_position()

    def run(self):
        if not self.freeze:
            if self.iterations >= self.MAX_ITERATIONS or self.goal_reached:
                print("BLIND Path found, length:", str(len(self.path)), ", iters:", self.iterations, ", cost:", self.COST)
                self.freeze = True
                self.COST += 10**7
            else:
                self.iterations += 1

            # algo guts here
            self.calculate()

        self.update_gui()
        if self.delay != 0:
            time.sleep(self.delay)
        return True

    def calculate(self):
        x, y = self.head
        self.COST += 1
        self.head = self._find_best_neighbour((x, y))

        # check progress
        new_x, new_y = self.head
        goal_x, goal_y = self.world.get_goal_position()
        if new_x == goal_x and new_y == goal_y:
            self.goal_reached = True
            self.checked = []
            self._check_for_shorter_path()
        if new_x == x and new_y == y:
            self.RETURNS += 1
        else:
            self.path.append(self.head)
            self.checked.append(self.head)
            self.RETURNS = 0

        if self.RETURNS > 0:
            if len(self.path) > 2:
                self.head = self.path[-2]
                self.path = self.path[:-1]
            else:
                # self.checked = []
                self.path = []
                self.head = self.world.get_start_position()

    def _check_for_shorter_path(self):
        for i in range(len(self.path)):
            if i < len(self.path):
                position = self.path[i]
            else:
                break
            for j in range(i+2, len(self.path)):
                next_position = self.path[j]
                if self._is_neighbour(position, next_position):
                    before = self.path[:i]
                    before.append(position)
                    after = self.path[j:]
                    self.path = before + after
                    break

    def _is_neighbour(self, position_a, position_b):
        ax, ay = position_a
        bx, by = position_b
        dif_x = math.fabs(ax-bx)
        dif_y = math.fabs(ay-by)
        return dif_x <= 1 and dif_y <= 1 and self._is_at_cross(ax, ay, bx, by)

    def _find_best_neighbour(self, position):
        x, y = position
        best_x, best_y = x, y
        goal_x, goal_y = self.world.get_goal_position()
        best_distance = self.distance(x, y, goal_x, goal_y) + 40

        range1 = x-1, x, x+1
        range2 = y-1, y, y+1
        # randomize order of neighbours
        # if random.randint(1, 2) == 1:
        #     range1 = x+1, x, x-1
        # if random.randint(1, 2) == 1:
        #     range2 = y+1, y, y-1

        for a in range1:
            for b in range2:
                if self._is_in_dimensions(a, b):
                    if self._is_not_in_obstacle(a, b):
                        if self._is_at_cross(a, b, x, y):
                            current_distance = self.distance(a, b, goal_x, goal_y)
                            if current_distance < best_distance:
                                if (a, b) not in self.checked:
                                    best_distance = current_distance
                                    best_x, best_y = a, b
        return best_x, best_y

    def _is_in_dimensions(self, a, b):
        return 0 <= a < self.world.get_width() and 0 <= b < self.world.get_height()

    def _is_not_in_obstacle(self, a, b):
        return self.world.get_fields()[a, b] != 1

    def _is_at_cross(self, a, b, x, y):
        return True
        return (a == x or b == y) and (a != x or b != y)

    def distance(self, x1, y1, x2, y2):
        # city metric
        xdiff = math.fabs(x1 - x2)
        ydiff = math.fabs(y1 - y2)
        diagonal_dist = min(xdiff, ydiff)
        straight_dist = math.fabs(xdiff - ydiff)

        return diagonal_dist*math.sqrt(2) + straight_dist

        # return math.sqrt((x1-x2)**2 + (y1-y2)**2)

    def update_gui(self):
        self.gui.display_path(self.checked, (100, 100, 100))
        self.gui.display_path(self.path, (200, 200, 0))
        return

    def get_iterations(self):
        return self.iterations

    def get_name(self):
        return self.NAME
