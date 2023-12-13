import pygame
import socket
import copy

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 960
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

FPS = 45

PLAYER_SPEED = 5
PLAYER_MASS = 12
PLAYER_START_POS = (0, 200)

PLAYER_R = 25
rate=17.15/12.5


ARROW_R = 10
arrow_img=pygame.transform.scale(pygame.image.load('arrow.png'), (ARROW_R*2, ARROW_R*2))


bufferSize = 1024
screen = pygame.display.set_mode(SCREEN_SIZE)  # , pygame.FULLSCREEN)
clock = pygame.time.Clock()

def draw_text(text, *, center=None, size=None, color=None):
    font = pygame.font.Font("MaplestoryBold.ttf", size or 24)
    text = font.render(text, True, color or (255, 255, 255))
    if center is None:
        text_rect = text.get_rect()
        text_rect.centerx = SCREEN_WIDTH // 2
        text_rect.centery = SCREEN_HEIGHT // 2
    else:
        text_rect = text.get_rect(center=center)
    screen.blit(text, text_rect)

