from blind_search import BlindSearch
from best_first_search import BestFirstSearch
from wave_propagation import WavePropagation
import pygame
import time
from gui import Gui
from world import World

print("PATHFINDER")

width, height = 100, 100
TILE_SIZE = 6
initial_delay = 0

WORLD_WIDTH = int(width / TILE_SIZE)
WORLD_HEIGHT = int(height / TILE_SIZE)
print("World dimensions set to", WORLD_WIDTH, WORLD_HEIGHT)
world = World(WORLD_WIDTH, WORLD_HEIGHT)

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("PATHFINDER")

gui1 = Gui(width, height, screen, TILE_SIZE)
gui2 = Gui(width, height, screen, TILE_SIZE)
gui3 = Gui(width, height, screen, TILE_SIZE)

wavePropagation = WavePropagation(width, height, world, gui1)
blindSearch = BlindSearch(width, height, world, gui2)
bestFirstSearch = BestFirstSearch(width, height, world, gui3)


def test_algorithms():
    running = True
    started = True
    time.sleep(initial_delay)
    print("RUNNING")

    while running:
        if started:
            blindSearch.run()
            wavePropagation.run()
            bestFirstSearch.run()
            # caption = str(algorithm.get_name()) + " iterations:" + str(algorithm.get_iterations())
            # pygame.display.set_caption(caption)

        disrupted = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                disrupted = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    disrupted = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                started = True
        pygame.display.update()
        world.display(gui1)
        if disrupted:
            break
    print("DONE")


test_algorithms()
