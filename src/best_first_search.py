from gui import Gui
from world import World
import pygame
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
            else:
                self.iterations += 1

            # algo guts here
            self.calculate()

        self.update_gui()
        if self.delay != 0:
            time.sleep(self.delay)
        return True

    def calculate(self):
        time.sleep(0.3)

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
        # self.gui.display_path(self.visited, (100, 100, 100))
        self.gui.display_path(self.to_check, (100, 0, 100))
        self.gui.display_path(self.path, (0, 200, 200))
        return

    def get_iterations(self):
        return self.iterations

    def get_name(self):
        return self.NAME

    def print_all_steps(self):
        print("--- steps ---")
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
