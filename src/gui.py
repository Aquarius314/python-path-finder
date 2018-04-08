import pygame


class Gui:

    BACKGROUND_COLOR = (0, 0, 0)
    GRID_COLOR = (200, 200, 200)
    OBSTACLE_COLOR = (200, 0, 0)
    START_COLOR = (0, 200, 0)
    GOAL_COLOR = (0, 0, 200)
    STEP_COLOR = (200, 200, 0)

    def __init__(self, width, height, screen, tile_size):
        self.width = width
        self.height = height
        self.screen = screen
        self.tile = tile_size

    def clear(self):
        self.screen.fill(self.BACKGROUND_COLOR)

    def display_fields(self, walls, width, height):
        for wall in walls:
            pygame.draw.rect(self.screen, self.OBSTACLE_COLOR,
                    pygame.Rect((wall.x + 1) * self.tile, (wall.y + 1) * self.tile,
                                (wall.width) * self.tile, (wall.height) * self.tile))


    def _display_specific_field(self, position, color):
        x, y = position
        pygame.draw.rect(self.screen, color,
                         pygame.Rect(x*self.tile+self.tile, y*self.tile+self.tile, self.tile, self.tile))

    def display_start(self, position):
        self._display_specific_field(position, self.START_COLOR)

    def display_goal(self, position):
        self._display_specific_field(position, self.GOAL_COLOR)

    def display_step(self, position, color):
        x, y = position
        pygame.draw.rect(self.screen, color,
                         pygame.Rect(x*self.tile+self.tile, y*self.tile+self.tile, self.tile, self.tile))

    def display_path(self, path, color):
        for i in range(len(path)-1):
            position = path[i]
            self._display_specific_field(position, color)

        if len(path) > 0:
            self._display_specific_field(path[-1], (0, 220, 0))
