from random import randint

import pygame

from grid import TileGrid
from collapse_algorithm import collapse_tile, search_least_entropy


WIDTH = 1920
HEIGHT = 1080


if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode(size=(WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    pygame.display.set_caption("WFC")
    x, y = 38, 22
    grid = TileGrid(x, y)
    collapse_tile(randint(0, x - 1), randint(0, y - 1), grid)

    start = pygame.time.get_ticks()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(color=(0, 0, 0))

        grid.draw(screen)

        end = pygame.time.get_ticks()

        if end - start > 0:
            x, y = search_least_entropy(grid)
            if x == None and y == None:
                pass
            else:
                collapse_tile(x, y, grid)
            start = pygame.time.get_ticks()

        pygame.display.flip()

