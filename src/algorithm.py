from gui import Gui
from world import World
import pygame
import time


class Algorithm:

    MAX_ITERATIONS = 100000
    TILE_SIZE = 20
    path = []

    def __init__(self, width, height, screen):
        self.width = width
        self.height = height
        self.gui = Gui(width, height, screen)
        self.WORLD_WIDTH = int(width / self.TILE_SIZE)
        self.WORLD_HEIGHT = int(height / self.TILE_SIZE)
        print("World dimensions set to", self.WORLD_WIDTH, self.WORLD_HEIGHT)
        self.world = World(self.WORLD_WIDTH, self.WORLD_HEIGHT)
        self.iterations = 0

    def run(self):
        self.iterations += 1
        if self.iterations%1 == 0:
            print("running iteration nr", self.iterations)
        if self.iterations >= self.MAX_ITERATIONS:
            return False

        # algo guts here

        self.update_gui()
        time.sleep(0.1)
        return True

    def update_gui(self):
        # self.gui.display_grid(self.WORLD_WIDTH, self.WORLD_HEIGHT, self.TILE_SIZE)
        self.gui.display_fields(self.world.get_fields(), self.TILE_SIZE)
        self.gui.display_start(self.world.get_start_position(), self.TILE_SIZE)
        self.gui.display_goal(self.world.get_goal_position(), self.TILE_SIZE)
