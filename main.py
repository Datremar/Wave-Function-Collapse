import pygame

from grid import TileGrid

WIDTH = 510
HEIGHT = 510


if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode(size=(WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    pygame.display.set_caption("WFC")

    grid = TileGrid()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(color=(0, 0, 0))

        grid.draw(screen)

        pygame.display.flip()
