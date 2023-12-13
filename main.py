import threading
import pygame
from settings import *
from character import *
from sprite import *
from pygame.math import Vector2
from graphic_manager import timing_manager
from math import pi

screen.fill('#000000')

background = Sprite(Vector2(0, 0), pygame.image.load('background.png'), background_manager)

p1 = character(Vector2(200, 0))
p2 = character(Vector2(-200, 0))
mychar = p1
notmychar = [p2]
myport = 10001
serverport = 10000


class Client:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_message_to_server(self, message):
        self.client_socket.sendto(message.encode(), ('localhost', serverport))


client_socket = Client()


def listen():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('localhost', myport))

    while True:
        data, addr = server_socket.recvfrom(bufferSize)
        message = data.decode()
        message = message.split()
        if message[0] == 'status':
            char = eval(message[1])
            char.pos_center = Vector2(float(message[2]), float(message[3]))
            char.hp = int(message[4])
        elif message[0] == 'shot':
            char = eval(message[1])
            char.gun.shot(target=Vector2(float(message[2]), float(message[3])),
                          caster=char.pos_center)
        elif message[0] == 'gun':
            char=eval(message[1])
            setattr(char.gun, message[2], eval(message[3]))


threading.Thread(target=listen).start()

client_socket.send_message_to_server('1gun homing True')
client_socket.send_message_to_server('1gun knockback 3')
client_socket.send_message_to_server('1gun one_shot 10')
client_socket.send_message_to_server('1gun accuracy_range pi/5')

# mychar.gun.homing=True
# mychar.gun.knockback=3
# mychar.gun.one_shot=10
# mychar.gun.accuracy_range=pi/5


def main(*_):
    # game set





    move = [0, 0, 0, 0]
    while True:
        background_manager.draw(screen, mychar.pos_center)
        player_manager.draw(screen, mychar.pos_center)
        bullet_manager.draw(screen, mychar.pos_center)
        timing_manager.execute()
        bullet_manager.go()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    move[0] = 1
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    move[1] = 1
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    move[2] = 1
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    move[3] = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    move[0] = 0
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    move[1] = 0
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    move[2] = 0
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    move[3] = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                # p1.gun.shot(target=Vector2(event.pos)-center+p1.pos_center,
                #             caster=p1.pos_center)
                shot_pos = Vector2(event.pos) - center + mychar.pos_center
                client_socket.send_message_to_server(f'1shot {shot_pos.x} {shot_pos.y}')
        movement = Vector2((move[2] - move[3], move[1] - move[0]))
        if not (movement.x == 0 and movement.y == 0):
            movement = movement / movement.length()
        mychar.move(movement)
        for p in notmychar:
            p.move(Vector2(0, 0))
        client_socket.send_message_to_server(f'1status {mychar.pos_center.x} {mychar.pos_center.y} {mychar.hp}')
        clock.tick(FPS)

        pygame.display.update()




func = main

params = ()
while __name__ == "__main__":
    result = func(*params)
    func, params = result
