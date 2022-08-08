from random import choice

from grid import TileGrid
from tile_data import TILE_DATA

distribution_map = (
    (0, +1),
    (0, -1),
    (-1, 0),
    (+1, 0),
    (+1, +1),
    (+1, -1),
    (-1, +1),
    (-1, -1),
)


def distribute_info(x, y, grid):
    tile_type = grid.tiles[x][y].socket_type
    disallowed_sockets = TILE_DATA["Tiles"][tile_type]["disallowed_sockets"]
    for vector in distribution_map:
        if x + vector[0] > grid.height - 1 \
                or x + vector[0] < 0 \
                or y + vector[1] > grid.width - 1 \
                or y + vector[1] < 0:
            continue
        if grid.tiles[x + vector[0]][y + vector[1]].entropy == 0:
            continue
        grid.tiles[x + vector[0]][y + vector[1]].partial_collapse(exclusions=disallowed_sockets)


def make_weighted_choice(variants):
    weights = [TILE_DATA["Tiles"][str(variant)]["weight"] for variant in variants]

    possibilities = []

    for i, weight in enumerate(weights):
        for _ in range(weight):
            possibilities.append(variants[i])

    tile_choice = choice(possibilities)

    return tile_choice


def collapse_tile(x, y, grid: TileGrid):
    variants = grid.tiles[x][y].variants
    if not variants:
        grid.tiles[x][y].sprite.set_image("resources/images/test_images/Tile1.png")
        return

    tile_choice = make_weighted_choice(variants)

    grid.tiles[x][y].collapse_to(tile_choice)
    distribute_info(x, y, grid)


def search_least_entropy(grid):
    tile_x, tile_y, entropy = -1, -1, 100

    for x, row in enumerate(grid.tiles):
        for y, tile in enumerate(row):
            if tile.entropy == 0:
                continue
            if tile.entropy < entropy:
                tile_x = x
                tile_y = y
                entropy = tile.entropy

    if tile_x != -1 and tile_y != -1:
        return tile_x, tile_y
    else:
        return None, None
