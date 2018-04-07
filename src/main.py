from best_first_search import BestFirstSearch
from wave_propagation import WavePropagation
import pygame
import time
from gui import Gui
from world import World

print("PATHFINDER")

width, height = 700, 700
TILE_SIZE = 6
initial_delay = 0

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("PATHFINDER")

gui = Gui(width, height, screen, TILE_SIZE)
WORLD_WIDTH = int(width / TILE_SIZE)
WORLD_HEIGHT = int(height / TILE_SIZE)
print("World dimensions set to", WORLD_WIDTH, WORLD_HEIGHT)
world = World(WORLD_WIDTH, WORLD_HEIGHT)

wavePropagation = WavePropagation(width, height, world, gui)
bestFirstSearch = BestFirstSearch(width, height, world, gui)
print("RUNNING")
running = True
time.sleep(initial_delay)
while running:
    running = bestFirstSearch.run() and wavePropagation.run()
    disrupted = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            disrupted = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                disrupted = True
    pygame.display.update()
    if disrupted:
        break

print("DONE")
