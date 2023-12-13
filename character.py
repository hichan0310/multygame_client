import sprite
from sprite import *
from gun import gun


class character(sprite.Sprite):
    def __init__(self, position, player_num):
        super(character, self).__init__(position, pygame.transform.scale(pygame.image.load(f'player{player_num}.png'),
                                                                         (PLAYER_R * 2 * rate, PLAYER_R * 2 * rate)),
                                        sprite.player_manager)
        self.hp = 100
        self.movement_real = Vector2((0, 0))
        self.mass = PLAYER_MASS
        self.speed = PLAYER_SPEED
        self.gun = gun()
        self.angle = 0

    def hit(self, dmg):
        self.hp -= dmg

    def heal(self, heal):
        self.hp = min(self.hp + heal, 100)

    def die(self):
        self.sp_manager.remove_sprite(self)

    def move(self, movement: Vector2):
        movement *= self.speed
        movement_real = self.movement_real * 0.9 \
                        + movement * 0.1
        self.movement_real = movement_real
        self.pos_center += movement_real

    def force(self, F: Vector2):
        self.movement_real += F / self.mass

    def hp_up(self):
        self.hp += 20

    def draw(self, pos_center):
        img = pygame.transform.rotate(self.img, self.angle + 90)
        img_size = Vector2(img.get_size())
        screen.blit(img, self.pos_center - img_size / 2 - pos_center + center)
