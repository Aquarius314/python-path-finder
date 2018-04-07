from algorithm import Algorithm
import pygame
import time


print("PATHFINDER")

width, height = 700, 700
initial_delay = 0

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("PATHFINDER")
algorithm = Algorithm(width, height, screen)
print("RUNNING")
running = True
if initial_delay != 0:
    time.sleep(initial_delay)
while running:
    running = algorithm.run()
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
