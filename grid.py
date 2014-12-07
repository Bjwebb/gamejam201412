import sys
import pygame
import copy
pygame.init()

SIZE = WIDTH, HEIGHT = 800, 600
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

def grid(size, color):
    for i in range(1, WIDTH//size):
        pygame.draw.line(screen, color, (i*size, 0), (i*size, HEIGHT))
    for i in range(1, HEIGHT//size):
        pygame.draw.line(screen, color, (0, i*size), (WIDTH, i*size))

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

current_time = 0
history= [{'state':{'posX': 0, 'posY':0}, 'action': {'posX': 0, 'posY': 0}} for i in range(0, (WIDTH//100)*(HEIGHT//100))]

def bounds_check(key, new_value):
    if key in ['posX', 'posY']:
        if new_value <= 0 or new_value >= 10:
            return False
    return True


def action(key, value, current_time):
    history[current_time]['action'][key] = value
    for time, history_item in enumerate(history):
        if time >= current_time:
            for k, v in history_item['action'].items():
                if bounds_check(k, history_item['state'][k] + v):
                    history_item['state'][k] += v
            if time+1 < len(history):
                history[time+1]['state'] = copy.copy(history_item['state'])



while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_time += 1
                action('posX', -1, current_time)
            elif event.key == pygame.K_RIGHT:
                #if pos[0] < 9:
                current_time += 1
                action('posX', +1, current_time)
            elif event.key == pygame.K_UP:
                #if pos[1] > 0:
                current_time += 1
                action('posY', -1, current_time)
            elif event.key == pygame.K_DOWN:
                #if pos[1] < 9:
                current_time += 1
                action('posY', +1, current_time)
            elif event.key == pygame.K_BACKSPACE:
                current_time -= 1
    screen.fill(BLACK)
    for time, history_item in enumerate(history):
        state = history_item['state']
        pygame.draw.rect(screen, RED, [
                time%(WIDTH//100)*100+(state['posX']*10),
                time//(WIDTH//100)*100+(state['posY']*10),
                10,
                10
            ])
    grid(10, BLUE)
    grid(100, WHITE)
    pygame.draw.rect(screen, GREEN, [
            current_time%(WIDTH//100)*100,
            current_time//(WIDTH//100)*100,
            101,
            101
        ], 1)
    pygame.display.flip()
