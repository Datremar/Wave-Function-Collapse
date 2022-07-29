from json import load

from tile import Tile


class TileGrid:
    def __init__(self):
        self.tiles = []

        for x in range(10):
            row = []
            for y in range(10):
                tile = Tile()
                tile.set_pos(51 * x, 51 * y)
                row.append(tile)
            self.tiles.append(row)

    def draw(self, screen):
        for row in self.tiles:
            for tile in row:
                if tile is None:
                    continue

                tile.draw(screen)

    def __repr__(self):
        representation = ""
        for row in self.tiles:
            str_row = ""
            for tile in row:
                str_row += f"{tile.entropy} "
            str_row += "\n"
            representation += str_row

        return representation
