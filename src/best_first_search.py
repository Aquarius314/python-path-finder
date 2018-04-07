from gui import Gui
from world import World
import pygame
import time
import math


class BestFirstSearch:

    # BEST FIRST SEARCH ALGORITHM

    MAX_ITERATIONS = 100000
    TILE_SIZE = 6
    path = []
    checked = []

    RETURNS = 0
    delay = 0.0
    head = 0, 0
    reached_goal = False

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
        self.iterations += 1
        if self.iterations%1 == 0:
            print("running iteration nr", self.iterations)
        if self.iterations >= self.MAX_ITERATIONS:
            return False

        # algo guts here
        if not self.reached_goal:
            self.calculate()

        self.update_gui()
        if self.delay != 0:
            time.sleep(self.delay)
        return True

    def calculate(self):
        x, y = self.head

        self.head = self._find_best_neighbour((x, y))

        # check progress
        new_x, new_y = self.head
        goal_x, goal_y = self.world.get_goal_position()
        if new_x == goal_x and new_y == goal_y:
            self.reached_goal = True
        if new_x == x and new_y == y:
            print("NO PROGRESS MAAN WE STUCK")
            self.RETURNS += 1
        else:
            self.path.append(self.head)
            self.checked.append(self.head)
            if len(self.path) > 3:
                self._check_for_shorter_path()
            self.RETURNS = 0

        if self.RETURNS > 0 and len(self.path) > 2:
            self.head = self.path[-2]
            self.path = self.path[:-1]

    def _check_for_shorter_path(self):
        last_position = self.path[-1]
        for i in range(len(self.path)-2):
            position = self.path[i]
            if self._is_neighbour(last_position, position):
                self.path = self.path[:i+1]
                self.path.append(last_position)
                return

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
        for a in range(x-1, x+2):
            for b in range(y-1, y+2):
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
        return (a == x or b == y) and (a != x or b != y)

    def distance(self, x1, y1, x2, y2):
        return math.sqrt((x1-x2)**2 + (y1-y2)**2)

    def update_gui(self):
        self.gui.clear()
        self.gui.display_fields(self.world.get_fields(), self.world.get_width(), self.world.get_height())
        self.gui.display_start(self.world.get_start_position())
        self.gui.display_goal(self.world.get_goal_position())
        self.gui.display_path(self.checked, (100, 100, 100))
        self.gui.display_path(self.path, (200, 200, 0))
        return
