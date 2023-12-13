from arrow import arrow
from settings import *
from pygame import Vector2
from math import atan, pi
from graphic_manager import timing_manager
import random


class gun:
    def __init__(self):
        self.speed = 10
        self.atk = 10
        self.poison = 0
        self.homing = False
        self.knockback = 0
        self.one_shot = 1
        self.range = 600
        self.accuracy_range=pi/20

    def shot(self, target: Vector2, caster: Vector2):
        shot_vector = target - caster
        direction = pi / 2 if shot_vector.y > 0 else -pi / 2
        try:
            direction = atan(shot_vector.y / shot_vector.x)
        except:
            pass
        if shot_vector.x < 0:
            direction += pi
        for i in range(self.one_shot):
            a = arrow(position=caster + shot_vector / shot_vector.length() * (PLAYER_R + ARROW_R + 5),
                      speed=self.speed,
                      direction=direction+(random.random()-0.5)*self.accuracy_range,
                      poison=self.poison,
                      atk=self.atk,
                      homing=self.homing,
                      knockback=self.knockback)

            timing_manager.add_functions(lambda *_: a.kill(), self.range // self.speed, ())
