from random import randint

from grid import TileGrid
from tile_data import TILE_DATA

distribution_map_r1 = (
    (-1, +1), (0,  +1), (+1, +1),
    (-1,  0),           (+1,  0),
    (-1, -1), (0,  -1), (+1, -1)
)

distribution_map_r2 = (
    (-2, +2), (-1, +2), (0,  +2), (+1, +2), (+2, +2),
    (-2, +1),                               (+2, +1),
    (-2,  0),                               (+2,  0),
    (-2, -1),                               (+2, -1),
    (-2, -2), (-1, -2), (0,  -2), (+1, -2), (+2, -2)
)

to_collapse = []
contradictions = []


def search_lowest_entropy():
    global to_collapse

    if not to_collapse:
        return None

    i = randint(0, len(to_collapse) - 1)

    pos = to_collapse.pop(i)

    return pos


# def search_lowest_entropy(grid: TileGrid):
#     global to_collapse
#
#     if not to_collapse:
#         return None
#
#     pos = to_collapse.pop()
#
#     return pos


def set_as_contradicted(x: int, y: int, grid: TileGrid):
    global contradictions

    grid.tiles[x][y].set_contradicted()
    if (x, y) not in contradictions:
        contradictions.append((x, y))


def check_for_contradiction(x: int, y: int, grid: TileGrid):
    center_tile_socket = grid.tiles[x][y].socket_type
    center_tile_socket = int(center_tile_socket)

    for pos in distribution_map_r1:
        tx = x + pos[0]
        ty = y + pos[1]
        if tx >= grid.width or ty >= grid.height or tx < 0 or ty < 0:
            continue

        tile_socket = grid.tiles[tx][ty].socket_type
        allowed_sockets = TILE_DATA[tile_socket]["allowed_sockets"]

        if center_tile_socket not in allowed_sockets:
            set_as_contradicted(x, y, grid)
            return


def collapse_tile(x: int, y: int, grid: TileGrid):
    global contradictions

    if grid.tiles[x][y].is_collapsed():
        return
    grid.tiles[x][y].collapse()

    if grid.tiles[x][y].is_contradicted():
        if (x, y) not in contradictions:
            contradictions.append((x, y))

    check_for_contradiction(x, y, grid)


def propagate_info(x: int, y: int, grid: TileGrid):
    tile_type = grid.tiles[x][y].socket_type
    allowed_sockets = TILE_DATA[tile_type]["allowed_sockets"]

    global to_collapse
    recently_collapsed_tiles = []

    for pos in distribution_map_r1:
        tx, ty = x + pos[0], y + pos[1]
        if tx >= grid.width or ty >= grid.height or tx < 0 or ty < 0:
            continue

        if grid.tiles[tx][ty].is_collapsed():
            continue

        grid.tiles[tx][ty].reduce_entropy(allowed_sockets)

        if grid.tiles[x][y].is_contradicted():
            if (x, y) not in contradictions:
                contradictions.append((x, y))

        if grid.tiles[tx][ty].is_collapsed():
            recently_collapsed_tiles.append((tx, ty))
        elif (tx, ty) not in to_collapse:
            to_collapse.append((tx, ty))

    for tile in recently_collapsed_tiles:
        tx, ty = tile
        propagate_info(tx, ty, grid)


def iterate(grid: TileGrid):
    pos = search_lowest_entropy()
    if not pos:
        return False

    x, y = pos
    collapse_tile(x, y, grid)
    propagate_info(x, y, grid)

    return True


def gather_surrounding_info(x: int, y: int, grid: TileGrid):
    variants_around = []

    for pos in distribution_map_r2:
        tx = x + pos[0]
        ty = y + pos[1]
        if tx >= grid.width or ty >= grid.height or tx < 0 or ty < 0:
            continue

        if grid.tiles[tx][ty].is_collapsed():
            variants_around.append(grid.tiles[tx][ty].socket_type)

    if not variants_around:
        return list(range(5))

    allowed_sockets = set()

    for variant in variants_around:
        sockets = TILE_DATA[variant]["allowed_sockets"]
        for socket in sockets:
            allowed_sockets.add(socket)

    if not allowed_sockets:
        print("Tile confused at:", x, y)

    return list(allowed_sockets)


def entangle(x: int, y: int, grid: TileGrid):
    global to_collapse

    info = gather_surrounding_info(x, y, grid)

    grid.tiles[x][y].entangle(info)
    to_collapse.append((x, y))

    for pos in distribution_map_r1:
        tx = x + pos[0]
        ty = y + pos[1]
        if tx >= grid.width or ty >= grid.height or tx < 0 or ty < 0:
            continue

        grid.tiles[tx][ty].entangle(list(range(5)))
        to_collapse.append((tx, ty))


def solve_contradictions(grid: TileGrid):
    global contradictions

    print("Solving Contradictions")
    print("Contradictions:", contradictions)

    for pos in contradictions:
        contradictions.remove(pos)
        x, y = pos
        entangle(x, y, grid)


def collapse_random(grid: TileGrid):
    x, y = randint(0, grid.width - 1), randint(0, grid.height - 1)
    collapse_tile(x, y, grid)
    propagate_info(x, y, grid)


def collapse_to(x: int, y: int, tile_type: int, grid: TileGrid):
    grid.tiles[x][y].collapse_to(tile_type)
    propagate_info(x, y, grid)


def collapse_chosen(x: int, y: int, grid: TileGrid):
    collapse_tile(x, y, grid)
    propagate_info(x, y, grid)
