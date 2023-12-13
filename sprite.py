import pygame
from pygame.math import Vector2
from settings import *

center = Vector2((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))


class Sprite:
    def __init__(self, pos_center: Vector2, image: pygame.Surface, sp_manager):
        self.pos_center = pos_center
        self.img_size = Vector2(image.get_size())
        self.img = image
        self.sp_manager: sprite_manager = sp_manager
        self.sp_manager.add_sprite(self)

    def go(self):
        pass

    def kill(self):
        self.sp_manager.remove_sprite(self)

    def draw(self, pos_center):
        screen.blit(self.img, self.pos_center - self.img_size / 2 - pos_center + center)


class sprite_manager:
    def __init__(self):
        self.sprites: list[Sprite] = []

    def add_sprite(self, sp):
        self.sprites.append(sp)

    def draw(self, screen: pygame.Surface, pos_center: Vector2):
        for sp in self.sprites:
            sp.draw(pos_center)

    def remove_sprite(self, sp):
        try:
            self.sprites.remove(sp)
        except:
            pass

    def go(self):
        for sp in self.sprites:
            sp.go()


background_manager = sprite_manager()
bullet_manager = sprite_manager()
player_manager = sprite_manager()
