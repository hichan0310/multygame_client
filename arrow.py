import pygame
import sprite
from settings import *
from pygame.math import Vector2
from sprite import *
from graphic_manager import timing_manager
from math import sin, cos, tan, pi


class arrow(sprite.Sprite):
    def __init__(self, position: Vector2, speed: int, direction: float,
                 poison: int = 0,
                 atk: float = 10.0,
                 homing: bool = False,
                 knockback: int = 0):
        super(arrow, self).__init__(pos_center=position,
                                    image=arrow_img,
                                    sp_manager=sprite.bullet_manager)
        self.speed = speed
        self.direction = direction
        self.poison = poison
        self.atk = atk
        self.homing = homing
        self.knockback = knockback

    def hit_character(self, character):
        return (self.pos_center - character.pos_center).length() < ARROW_R + PLAYER_R

    def go(self):
        direction_vector = Vector2((cos(self.direction), sin(self.direction)))
        for player in player_manager.sprites:
            if self.hit_character(player):
                player.hit(self.atk)
                tmp = direction_vector * self.knockback
                timing_manager.add_functions(lambda p: p.force(tmp), 0, (player,))
                timing_manager.add_functions(lambda p: p.force(tmp), 1, (player,))
                timing_manager.add_functions(lambda p: p.force(tmp), 2, (player,))
                timing_manager.add_functions(lambda p: p.force(tmp), 3, (player,))
                self.kill()
        speed = self.speed * direction_vector
        self.pos_center += speed
        if self.homing:
            def theta(p):
                x = p.pos_center - self.pos_center
                l=x.length()
                return speed.dot(x / l) / self.speed * 200 / l

            target = sorted(player_manager.sprites, key=theta, reverse=True)[0]
            if theta(target) > 0.5:
                target_vector = target.pos_center - self.pos_center
                if target_vector.x * speed.y - target_vector.y * speed.x > 0:
                    self.direction -= pi / 120
                else:
                    self.direction += pi / 120
