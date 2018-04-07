import pygame


class Gui:

    BACKGROUND_COLOR = (0, 0, 0)
    GRID_COLOR = (200, 200, 200)
    OBSTACLE_COLOR = (200, 0, 0)
    START_COLOR = (0, 200, 0)
    GOAL_COLOR = (0, 0, 200)
    STEP_COLOR = (200, 200, 0)

    def __init__(self, width, height, screen):
        self.width = width
        self.height = height
        self.screen = screen

    def clear(self):
        self.screen.fill(self.BACKGROUND_COLOR)

    def display_fields(self, fields, tile, width, height):
        for x in range(width):
            for y in range(height):
                if fields[x, y] == 1:
                    pygame.draw.rect(self.screen, self.OBSTACLE_COLOR,
                                     pygame.Rect((x+1)*tile, (y+1)*tile, tile, tile))

    def _display_specific_field(self, position, color, tile, size=0):
        x, y = position
        pygame.draw.rect(self.screen, color,
                         pygame.Rect(x*tile+tile-size, y*tile+tile-size, tile+size*2, tile+size*2))

    def display_start(self, position, tile):
        self._display_specific_field(position, self.START_COLOR, tile, 2)

    def display_goal(self, position, tile):
        self._display_specific_field(position, self.GOAL_COLOR, tile, 2)

    def display_step(self, position, tile, color):
        x, y = position
        pygame.draw.rect(self.screen, color,
                         pygame.Rect(x*tile+tile, y*tile+tile, tile, tile))
