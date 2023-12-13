import threading
import pygame
from settings import *
from character import *
from sprite import *
from pygame.math import Vector2
from graphic_manager import timing_manager
from math import pi

pygame.init()

player_amount = 2
player_number = 1

screen.fill('#000000')

background = Sprite(Vector2(0, 0), pygame.image.load('background.png'), background_manager)

p1 = character(Vector2(200, 0), player_num=1)
p2 = character(Vector2(-200, 0), player_num=2)
mychar: character = eval(f'p{player_number}')
notmychar = [eval(f'p{i}') for i in range(1, player_amount + 1) if i != player_number]
myport = 10000 + player_number
serverport = 10000


class Client:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_message_to_server(self, message):
        self.client_socket.sendto(message.encode(), ('localhost', serverport))


client_socket = Client()

end=True
win=None
def listen():
    global end, win
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
            char = eval(message[1])
            setattr(char.gun, message[2], eval(message[3]))
        elif message[0] == 'end':
            win=message[1]
            end=True


def main(*_):
    screen.fill('#000000')
    # game set
    client_socket.send_message_to_server(f'ready {player_number}')
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('localhost', myport))
    draw_text('waiting for other players...')
    pygame.display.update()
    while True:
        pygame.event.get()
        clock.tick(FPS)
        data, addr = server_socket.recvfrom(bufferSize)
        message = data.decode()
        if message == 'start':
            break
    server_socket.close()

    threading.Thread(target=listen).start()

    # gun set
    client_socket.send_message_to_server(f'{player_number}gun homing True')
    client_socket.send_message_to_server(f'{player_number}gun knockback 3')
    client_socket.send_message_to_server(f'{player_number}gun one_shot 10')
    client_socket.send_message_to_server(f'{player_number}gun accuracy_range pi/5')
    #client_socket.send_message_to_server(f'{player_number}gun atk 0')

    move = [0, 0, 0, 0]
    while True:
        background_manager.draw(screen, mychar.pos_center)
        player_manager.draw(screen, mychar.pos_center)
        bullet_manager.draw(screen, mychar.pos_center)
        timing_manager.execute()
        bullet_manager.go()
        if end:
            break
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
                client_socket.send_message_to_server(f'{player_number}shot {shot_pos.x} {shot_pos.y}')

        direction = pygame.mouse.get_pos() - center
        radius, angle = direction.as_polar()
        mychar.angle = 180 - angle

        movement = Vector2((move[2] - move[3], move[1] - move[0]))
        if not (movement.x == 0 and movement.y == 0):
            movement = movement / movement.length()
        mychar.move(movement)
        for p in notmychar:
            p.move(Vector2(0, 0))
        client_socket.send_message_to_server(
            f'{player_number}status {mychar.pos_center.x} {mychar.pos_center.y} {mychar.hp}')
        clock.tick(FPS)

        pygame.display.update()
    screen.fill('#000000')
    draw_text(f'{win} win')
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                return main, _


def start(*_):
    print('asdf')
    while True:
        background_manager.draw(screen, center)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print('start')
                    return main, _

        clock.tick(FPS)
        pygame.display.update()


func = main

params = ()
while __name__ == "__main__":
    end=False
    result = func(*params)
    func, params = result
