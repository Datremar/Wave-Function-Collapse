import pygame

from collapse_algorithm import collapse_random, iterate, collapse_chosen, solve_contradictions, entangle
from grid import TileGrid

WIDTH = 1920
HEIGHT = 1080

if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode(size=(WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    pygame.display.set_caption("WFC")

    x, y = 38, 22
    grid = TileGrid(x, y)
    collapse_random(grid)
    collapse_random(grid)
    collapse_random(grid)

    start = pygame.time.get_ticks()

    running = True
    should_collapse = False
    contradicted = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    should_collapse = True
            if not should_collapse and event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    x, y = mouse_pos
                    x = x // 51
                    y = y // 51

                    collapse_chosen(x, y, grid)
            if not should_collapse and event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    mouse_pos = pygame.mouse.get_pos()
                    x, y = mouse_pos
                    x = x // 51
                    y = y // 51

                    entangle(x, y, grid)
                    should_collapse = True

        screen.fill(color=(0, 0, 0))

        grid.draw(screen)

        end = pygame.time.get_ticks()

        if should_collapse:
            if end - start > 0:
                should_collapse = iterate(grid)
                start = pygame.time.get_ticks()
        else:
            should_collapse = False
            contradicted = True

        if contradicted:
            solve_contradictions(grid)
            should_collapse = True
            contradicted = False

        pygame.display.flip()
