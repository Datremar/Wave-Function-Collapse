import pygame


class TileSprite:
    def __init__(self, image_path: str = ""):
        self.x = 0
        self.y = 0

        if image_path == "":
            self.image = pygame.image.load("resources/images/TestTile.png")
        else:
            self.image = pygame.image.load(image_path)

    def set_pos(self, x, y):
        self.x = x
        self.y = y
        print(self)

    def draw(self, screen):
        # print(self)
        screen.blit(self.image, self.image.get_rect().move(self.x, self.y))

    def __repr__(self):
        return f"{self.x}, {self.y}"


if __name__ == "__main__":
    tile = TileSprite()
    print(tile)
    tile.set_pos(1, 1)
    print(tile)
