# Copyright (c) 2014 Ben Webb http://bjwebb.co.uk/
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
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
player_img = pygame.image.load('instant_dungeon_artpack/By Scott Matott/Players.png')
stone_img = pygame.image.load('instant_dungeon_artpack/By Scott Matott/stone_bricks.png')
gems_img = pygame.image.load('instant_dungeon_artpack/By Scott Matott/torch_key_gems.png')
font = pygame.font.Font(None, 36)

WALLS = [
    ' #        ',
    '   ## ####',
    '###       ',
    '    #### #',
    ' ###   # #',
    ' # # # ###',
    ' # # #    ',
    ' #   # ## ',
    ' # ###  ##',
    '      #   ',
]

def grid(size, color):
    for i in range(1, WIDTH//size):
        pygame.draw.line(screen, color, (i*size, 0), (i*size, HEIGHT))
    for i in range(1, HEIGHT//size):
        pygame.draw.line(screen, color, (0, i*size), (WIDTH, i*size))

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

current_time = 0
history= [{'state':{'posX': 0, 'posY':0}, 'action': {'posX': 0, 'posY': 0}} for i in range(0, (WIDTH//(WORLD_SIZE*SPRITE_SIZE))*(HEIGHT//(WORLD_SIZE*SPRITE_SIZE)))]

def bounds_check(state):
    for key in ['posX', 'posY']:
        if state[key] < 0 or state[key] >= WORLD_SIZE:
            return False
    if WALLS[state['posY']][state['posX']] == '#':
        return False
    return True


def action(key, value, current_time):
    if current_time >= len(history):
        return
    history[current_time]['action'][key] = value
    for time, history_item in enumerate(history):
        if time >= current_time:
            history_item['state'] = copy.copy(history[time-1]['state'])
            for k, v in history_item['action'].items():
                new_state = copy.copy(history_item['state'])
                new_state[k] += v
                if bounds_check(new_state):
                    history_item['state'] = new_state

def pos_to_pixel_x(pos, time):
    return time%(WIDTH//(WORLD_SIZE*SPRITE_SIZE))*(WORLD_SIZE*SPRITE_SIZE)+(pos*SPRITE_SIZE)

def pos_to_pixel_y(pos, time):
    return time//(WIDTH//(WORLD_SIZE*SPRITE_SIZE))*(WORLD_SIZE*SPRITE_SIZE)+(pos*SPRITE_SIZE)

while 1:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_time += 1
                action('posY', 0, current_time)
                action('posX', -1, current_time)
                pygame.mixer.music.load('254316__jagadamba__clock-tick.wav')
                pygame.mixer.music.play()
            elif event.key == pygame.K_RIGHT:
                current_time += 1
                action('posY', 0, current_time)
                action('posX', +1, current_time)
                pygame.mixer.music.load('254316__jagadamba__clock-tick.wav')
                pygame.mixer.music.play()
            elif event.key == pygame.K_UP:
                current_time += 1
                action('posX', 0, current_time)
                action('posY', -1, current_time)
                pygame.mixer.music.load('254316__jagadamba__clock-tick.wav')
                pygame.mixer.music.play()
            elif event.key == pygame.K_DOWN:
                current_time += 1
                action('posX', 0, current_time)
                action('posY', +1, current_time)
                pygame.mixer.music.load('254316__jagadamba__clock-tick.wav')
                pygame.mixer.music.play()
            elif event.key == pygame.K_SPACE:
                current_time += 1
                action('posX', 0, current_time)
                action('posY', 0, current_time)
                pygame.mixer.music.load('254316__jagadamba__clock-tick.wav')
                pygame.mixer.music.play()
            elif event.key == pygame.K_BACKSPACE:
                current_time -= 1
                pygame.mixer.music.load('162493__tasmanianpower__vinyl-rewind.wav')
                pygame.mixer.music.play()
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            new_time = (pos[0]//(WORLD_SIZE*SPRITE_SIZE)) + (WIDTH//(WORLD_SIZE*SPRITE_SIZE)) * (pos[1]//(WORLD_SIZE*SPRITE_SIZE))
            if new_time < current_time:
                pygame.mixer.music.load('162493__tasmanianpower__vinyl-rewind.wav')
                pygame.mixer.music.play()
            current_time = new_time
    screen.fill(BLACK)
    for time, history_item in enumerate(history):
        state = history_item['state']
        screen.blit(player_img, (
                pos_to_pixel_x(state['posX'], time),
                pos_to_pixel_y(state['posY'], time),
            ), (0, 0, 16, 16))
        for x in range(state['posX']-2, state['posX']+3):
            if x < 0 or x >= WORLD_SIZE:
                continue
            for y in range(state['posY']-2, state['posY']+3):
                if y < 0 or y >= WORLD_SIZE:
                    continue
                if WALLS[y][x] == '#':
                    screen.blit(stone_img, (
                            pos_to_pixel_x(x, time),
                            pos_to_pixel_y(y, time),
                        ), (0, 0, 16, 16))
        if state['posX'] == WORLD_SIZE-1 and state['posY'] == WORLD_SIZE-1:
            text = font.render('You Win!', 1, WHITE)
            screen.blit(text, (
                pos_to_pixel_x(WORLD_SIZE//2, time) - text.get_rect().centerx,
                pos_to_pixel_y(WORLD_SIZE//2, time) - text.get_rect().centery))
        elif time == len(history) -1:
            text = font.render('You Lose!', 1, WHITE)
            screen.blit(text, (
                pos_to_pixel_x(WORLD_SIZE//2, time) - text.get_rect().centerx,
                pos_to_pixel_y(WORLD_SIZE//2, time) - text.get_rect().centery))
        screen.blit(gems_img, (
                pos_to_pixel_x(WORLD_SIZE-1, time),
                pos_to_pixel_y(WORLD_SIZE-1, time),
            ), (6*16, 16, 16, 16))
    #grid(SPRITE_SIZE, BLUE)
    grid(SPRITE_SIZE*WORLD_SIZE, WHITE)
    pygame.draw.rect(screen, GREEN, [
            pos_to_pixel_x(0, current_time),
            pos_to_pixel_y(0, current_time),
            WORLD_SIZE*SPRITE_SIZE+1,
            WORLD_SIZE*SPRITE_SIZE+1
        ], 1)
    pygame.display.flip()

