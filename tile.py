import pygame

from tile_data import TILE_DATA


class TileSprite:
    def __init__(self, image_path: str = ""):
        self.x = 0
        self.y = 0

        if image_path == "":
            self.image = pygame.image.load("resources/images/test_images/TestTile.png")
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
        self.socket_type = "-1"
        self.sprite = TileSprite()
        self.variants = list(range(5))
        self.entropy = len(self.variants)

        self.sprite.set_image("resources/images/blurs/uncertain.png")

    @classmethod
    def get_sprite_name(cls, tile_id):
        return TILE_DATA['Tiles'][str(tile_id)]['sprite']

    def partial_collapse(self, exclusions=None, inclusions=None):
        if self.entropy == 0:
            return

        if exclusions and not inclusions:
            for exclusion in exclusions:
                if exclusion in self.variants:
                    self.variants.remove(exclusion)
        elif inclusions and not exclusions:
            for variant in self.variants:
                if variant not in inclusions:
                    self.variants.remove(variant)

        self.entropy = len(self.variants)

        if self.entropy == 0:
            pass
        elif self.entropy == 1:
            self.socket_type = self.variants[0]
            self.sprite.set_image(f"resources/images/sprites/{Tile.get_sprite_name(self.socket_type)}")

            self.variants.clear()
            self.entropy = 0
        elif 1 < self.entropy < 5:
            blur_id = "".join(map(str, self.variants))
            self.sprite.set_image(f"resources/images/blurs/{blur_id}.png")
        else:
            self.sprite.set_image("resources/images/blurs/uncertain.png")

    def collapse_to(self, tile_id):
        self.entropy = 0
        self.variants = []
        self.socket_type = str(tile_id)

        self.sprite.set_image(f"resources/images/sprites/{Tile.get_sprite_name(self.socket_type)}")

    def set_pos(self, x, y):
        self.sprite.set_pos(x, y)

    def draw(self, screen):
        self.sprite.draw(screen)

    def __repr__(self):
        return f"{self.entropy} {self.variants} {self.sprite.__repr__()}"
