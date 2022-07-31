import pygame

from tile_data import TILE_DATA


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

    def set_image(self, image_path):
        self.image = pygame.image.load(image_path)

    def draw(self, screen):
        screen.blit(self.image, self.image.get_rect().move(self.x, self.y))

    def __repr__(self):
        return f"{self.x}, {self.y}"


class Tile:
    def __init__(self):
        self.type = "-1"
        self.sprite = TileSprite()
        self.variants = list(range(5))
        self.entropy = len(self.variants)

        self.sprite.set_image("resources/images/uncertain.png")

    @classmethod
    def get_sprite_name(cls, tile_id):
        return TILE_DATA['Tiles'][str(tile_id)]['sprite']

    def collapse(self, *variants_to_exclude):
        for exclusion in variants_to_exclude:
            if exclusion in self.variants:
                self.variants.remove(exclusion)

        self.entropy = len(self.variants)

        if self.entropy == 0:
            pass
        if self.entropy == 1:
            self.type = self.variants[0]
            self.sprite.set_image(f"resources/images/{Tile.get_sprite_name(self.type)}")

            self.variants.clear()
            self.entropy = 0
        else:
            self.sprite.set_image("resources/images/uncertain.png")

    def set_pos(self, x, y):
        self.sprite.set_pos(x, y)

    def draw(self, screen):
        self.sprite.draw(screen)

    def __repr__(self):
        return f"{self.entropy} {self.variants} {self.sprite.__repr__()}"
