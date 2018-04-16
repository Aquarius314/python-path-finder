from gui import Gui
from world import World
import time
import math
import random
import numpy as np


class Node:

    def __init__(self, parent_x, parent_y, distance):
        self.parent_x = parent_x
        self.parent_y = parent_y
        self.distance = distance

class BestFirstSearch:

    NAME = "Best First Search"
    MAX_ITERATIONS = 100000
    COST = 0.0
    TILE_SIZE = 6
    freeze = False

    steps = []
    to_check = []
    visited = []
    path = []
    parents = []

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
        self.rewrite_world_to_steps_array()
        self.head = self.world.get_start_position()
        self.to_check.append(self.head)

    def rewrite_world_to_steps_array(self):
        goal_x, goal_y = self.world.get_goal_position()
        self.steps = np.zeros(self.world.get_size())
        self.parents = np.zeros(self.world.get_size())
        for y in range(self.world.get_width()):
            for x in range(self.world.get_height()):
                if self.world.get_field_value(x, y) == 1:
                    self.steps[x, y] = -1
                else:
                    self.steps[x, y] = self.distance(x, y, goal_x, goal_y)
        # rewrite start and goal positions
        goal_x, goal_y = self.world.get_goal_position()
        self.steps[goal_x, goal_y] = 0

    def run(self):
        if not self.freeze:
            if self.iterations >= self.MAX_ITERATIONS or self.goal_reached:
                print("BFS Path found, length:", str(len(self.path)), ", iters:", self.iterations, ", cost:", self.COST)
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

        new_iteration = []

        best_node_distance = self.steps[self.to_check[0]]
        for node in self.to_check:
            if self.steps[node] < best_node_distance:
                best_node_distance = self.steps[node]

        for node in self.to_check:
            if node not in self.visited and self.steps[node] == best_node_distance:
                new_iteration.append(node)

        # propagate new nodes
        self.COST += len(new_iteration)
        for node in new_iteration:
            self._propagate(node)
            self.visited.append(node)

        # clear visited nodes from "to check"
        for node in self.visited:
            if node in self.to_check:
                self.to_check.remove(node)

        # check if goal reached
        for node in self.to_check:
            if self.steps[node] == 0:
                self.goal_reached = True
                self.path = self._define_path()
                break

    def _define_path(self):
        # self.print_all_steps(self.parents)
        x, y = self.world.get_goal_position()
        path = [(x, y)]
        start_x, start_y = self.world.get_start_position()
        while True:
            parent = self.parents[x, y]
            move_x, move_y = self._decode_parent(parent)
            if move_x == 0 and move_y == 0:
                return path
            x += move_x
            y += move_y
            path.append((x, y))
            if x == start_x and y == start_y:
                break
        return path

    def _propagate(self, node):
        x, y = node
        for a in range(x-1, x+2):
            for b in range(y-1, y+2):
                if not self._is_in_dimensions(a, b):
                    continue
                if not self._is_not_in_obstacle(a, b):
                    continue
                if a == x and b == y:
                    continue
                if (a, b) not in self.to_check:
                    self.to_check.append((a, b))
                    if self.parents[a, b] == 0:
                        self.parents[a, b] = self._define_parent(a-x, b-y)

    def _decode_parent(self, parent):
        if parent == 1:
            return 1, 1
        if parent == 2:
            return 0, 1
        if parent == 3:
            return -1, 1
        if parent == 4:
            return 1, 0
        if parent == 5:
            return -1, 0
        if parent == 6:
            return 1, -1
        if parent == 7:
            return 1, 0
        if parent == 8:
            return -1, -1
        return -1, -1

    def _define_parent(self, a, b):
        if a == -1:
            if b == -1:
                return 1
            if b == 0:
                return 4
            if b == 1:
                return 6
        if a == 0:
            if b == -1:
                return 2
            if b == 0:
                return 0
            if b == 1:
                return 7
        if a == 1:
            if b == -1:
                return 3
            if b == 0:
                return 5
            if b == 1:
                return 8

    def _is_neighbour(self, position_a, position_b):
        ax, ay = position_a
        bx, by = position_b
        dif_x = math.fabs(ax-bx)
        dif_y = math.fabs(ay-by)
        return dif_x <= 1 and dif_y <= 1 and self._is_at_cross(ax, ay, bx, by)

    def _is_in_dimensions(self, a, b):
        return 0 <= a < self.world.get_width() and 0 <= b < self.world.get_height()

    def _is_not_in_obstacle(self, a, b):
        return self.world.get_fields()[a, b] != 1

    def _is_at_cross(self, a, b, x, y):
        return True
        return (a == x or b == y) and (a != x or b != y)

    def distance_points(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        return self.distance(x1, y1, x2, y2)

    def distance(self, x1, y1, x2, y2):
        # city metric
        xdiff = math.fabs(x1 - x2)
        ydiff = math.fabs(y1 - y2)
        diagonal_dist = min(xdiff, ydiff)
        straight_dist = math.fabs(xdiff - ydiff)
        return diagonal_dist*math.sqrt(2) + straight_dist

    def update_gui(self):
        self.gui.display_path(self.visited, (100, 100, 100))
        self.gui.display_path(self.to_check, (100, 0, 100))
        self.gui.display_path(self.path, (0, 200, 200))
        return

    def get_iterations(self):
        return self.iterations

    def get_name(self):
        return self.NAME

    def print_all_steps(self, array):
        print("--- steps ---")
        for y in range(len(array)):
            line = ""
            for x in range(len(array[0])):
                if array[x, y] == -1:
                    line += "  *"
                else:
                    # if 10 > array[x, y] > -2:
                    #     line += " "
                    line += "|"
                    if int(array[x, y]) == 0:
                        line += "  "
                    if int(array[x, y]) == 1:
                        line += "RD"
                    if int(array[x, y]) == 2:
                        line += "DD"
                    if int(array[x, y]) == 3:
                       line += "LD"
                    if int(array[x, y]) == 4:
                        line += "RR"
                    if int(array[x, y]) == 5:
                        line += "LL"
                    if int(array[x, y]) == 6:
                        line += "RU"
                    if int(array[x, y]) == 7:
                        line += "UU"
                    if int(array[x, y]) == 8:
                        line += "LU"

            print(line)
