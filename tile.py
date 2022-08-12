from random import choice

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
        self.contradicted = False
        self.collapsed = False
        self.socket_type = "-1"
        self.sprite = TileSprite()
        self.variants = list(range(5))
        self.entropy = len(self.variants)

        self.sprite.set_image("resources/images/blurs/uncertain.png")

    @classmethod
    def get_sprite_name(cls, tile_id):
        return TILE_DATA[str(tile_id)]['sprite']

    def set_contradicted(self):
        self.sprite.set_image("resources/images/test_images/contradicted.png")
        self.collapsed = True
        self.contradicted = True
        print("CONTRADICTION OCCURED")

    def set_blur(self):
        blur_id = "".join(map(str, self.variants))
        if blur_id == "01234":
            blur_id = "uncertain"

        if blur_id != "":
            self.sprite.set_image(f"resources/images/blurs/{blur_id}.png")
        else:
            self.set_contradicted()

    def reduce_entropy(self, allowed_variants):
        if self.collapsed:
            return

        variants_to_remove = []

        for variant in self.variants:
            if variant not in allowed_variants:
                variants_to_remove.append(variant)

        for variant in variants_to_remove:
            self.variants.remove(variant)

        self.entropy = len(self.variants)

        if self.entropy == 0:
            self.set_contradicted()
            return

        if self.entropy == 1:
            self.collapse_to(self.variants[0])
        else:
            self.set_blur()

    def collapse_to(self, tile_id):
        self.entropy = 0
        self.variants = []
        self.collapsed = True
        self.socket_type = str(tile_id)

        self.sprite.set_image(f"resources/images/sprites/{Tile.get_sprite_name(self.socket_type)}")

    def collapse(self):
        collapse_choice = choice(self.variants)
        self.collapse_to(collapse_choice)

    def entangle(self, variants: list):
        self.collapsed = False
        self.contradicted = False
        self.variants = variants
        self.entropy = len(self.variants)

        self.set_blur()

    def is_collapsed(self):
        return self.collapsed

    def is_contradicted(self):
        return self.contradicted

    def set_pos(self, x, y):
        self.sprite.set_pos(x, y)

    def draw(self, screen):
        self.sprite.draw(screen)

    def __repr__(self):
        return f"{self.entropy} {self.variants} {self.sprite.__repr__()}"
