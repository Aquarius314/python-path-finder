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

    def display_grid(self, x, y, tile):
        for i in range(x+1):
            pygame.draw.line(self.screen, self.GRID_COLOR, (i*tile, 0), (i*tile, self.height))
        for i in range(y+1):
            pygame.draw.line(self.screen, self.GRID_COLOR, (0, i*tile), (self.width, i*tile))

    def display_fields(self, fields, tile):
        for x in range(len(fields)):
            for y in range(len(fields[0])):
                if fields[x, y] == 1:
                    pygame.draw.rect(self.screen, self.OBSTACLE_COLOR,
                                     pygame.Rect(x*tile, y*tile, tile, tile))

    def _display_specific_field(self, position, color, tile):
        x, y = position
        pygame.draw.circle(self.screen, color, (int(x*tile+tile/2-2), int(y*tile+tile/2-2)), int(tile/2+2))

    def display_start(self, position, tile):
        self._display_specific_field(position, self.START_COLOR, tile)

    def display_goal(self, position, tile):
        self._display_specific_field(position, self.GOAL_COLOR, tile)

    def display_step(self, position, tile):
        x, y = position
        pygame.draw.circle(self.screen, self.STEP_COLOR,
                           (int(x*tile+tile/2), int(y*tile+tile/2)), int(tile/3))
