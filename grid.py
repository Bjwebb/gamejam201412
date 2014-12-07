import sys
import pygame
import copy
pygame.init()

SIZE = WIDTH, HEIGHT = 1440, 800
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)
LIGHT_RED =   (255,   128,   128)
SPRITE_SIZE = 16
WORLD_SIZE = 10

def grid(size, color):
    for i in range(1, WIDTH//size):
        pygame.draw.line(screen, color, (i*size, 0), (i*size, HEIGHT))
    for i in range(1, HEIGHT//size):
        pygame.draw.line(screen, color, (0, i*size), (WIDTH, i*size))

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

current_time = 1
history= [{'state':{'posX': 0, 'posY':0}, 'action': {'posX': 0, 'posY': 0}} for i in range(0, (WIDTH//(WORLD_SIZE*SPRITE_SIZE))*(HEIGHT//(WORLD_SIZE*SPRITE_SIZE)))]

def bounds_check(key, new_value):
    if key in ['posX', 'posY']:
        if new_value < 0 or new_value >= WORLD_SIZE:
            return False
    return True


def action(key, value, current_time):
    history[current_time]['action'][key] = value
    for time, history_item in enumerate(history):
        if time >= current_time:
            history_item['state'] = copy.copy(history[time-1]['state'])
            for k, v in history_item['action'].items():
                if bounds_check(k, history_item['state'][k] + v):
                    history_item['state'][k] += v



while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                #current_time += 1
                action('posY', 0, current_time)
                action('posX', -1, current_time)
            elif event.key == pygame.K_RIGHT:
                #current_time += 1
                action('posY', 0, current_time)
                action('posX', +1, current_time)
            elif event.key == pygame.K_UP:
                #current_time += 1
                action('posX', 0, current_time)
                action('posY', -1, current_time)
            elif event.key == pygame.K_DOWN:
                #current_time += 1
                action('posX', 0, current_time)
                action('posY', +1, current_time)
            elif event.key == pygame.K_DELETE:
                action('posX', 0, current_time)
                action('posY', 0, current_time)
            elif event.key == pygame.K_BACKSPACE:
                current_time -= 1
            elif event.key == pygame.K_SPACE:
                current_time += 1
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            new_time = (pos[0]//(WORLD_SIZE*SPRITE_SIZE)) + (WIDTH//(WORLD_SIZE*SPRITE_SIZE)) * (pos[1]//(WORLD_SIZE*SPRITE_SIZE))
            if new_time > 0:
                current_time = new_time
    screen.fill(BLACK)
    for time, history_item in enumerate(history):
        state = history_item['state']
        if time > 0:
            pygame.draw.rect(screen, LIGHT_RED, [
                    time%(WIDTH//(WORLD_SIZE*SPRITE_SIZE))*(WORLD_SIZE*SPRITE_SIZE)+(history[time-1]['state']['posX']*SPRITE_SIZE),
                    time//(WIDTH//(WORLD_SIZE*SPRITE_SIZE))*(WORLD_SIZE*SPRITE_SIZE)+(history[time-1]['state']['posY']*SPRITE_SIZE),
                    SPRITE_SIZE,
                    SPRITE_SIZE
                ])
        pygame.draw.rect(screen, RED, [
                time%(WIDTH//(WORLD_SIZE*SPRITE_SIZE))*(WORLD_SIZE*SPRITE_SIZE)+(state['posX']*SPRITE_SIZE),
                time//(WIDTH//(WORLD_SIZE*SPRITE_SIZE))*(WORLD_SIZE*SPRITE_SIZE)+(state['posY']*SPRITE_SIZE),
                SPRITE_SIZE,
                SPRITE_SIZE
            ])
    grid(SPRITE_SIZE, BLUE)
    grid(SPRITE_SIZE*WORLD_SIZE, WHITE)
    pygame.draw.rect(screen, GREEN, [
            current_time%(WIDTH//(WORLD_SIZE*SPRITE_SIZE))*(WORLD_SIZE*SPRITE_SIZE),
            current_time//(WIDTH//(WORLD_SIZE*SPRITE_SIZE))*(WORLD_SIZE*SPRITE_SIZE),
            WORLD_SIZE*SPRITE_SIZE+1,
            WORLD_SIZE*SPRITE_SIZE+1
        ], 1)
    pygame.display.flip()
