from tile import Tile


class TileGrid:
    def __init__(self, width, height):
        self.tiles = []
        self.height = width
        self.width = height

        for x in range(self.height):
            row = []
            for y in range(self.width):
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
