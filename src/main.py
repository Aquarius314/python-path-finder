from algorithm import Algorithm
import pygame


print("PATHFINDER")

width, height = 800, 800

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("PATHFINDER")
algorithm = Algorithm(width, height, screen)
print("RUNNING")
running = True
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
