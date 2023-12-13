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
ARROW_R = 10

bufferSize = 1024
screen = pygame.display.set_mode(SCREEN_SIZE)  # , pygame.FULLSCREEN)
clock = pygame.time.Clock()
