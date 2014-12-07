import sys, pygame
pygame.init()

size = width, height = 800, 600
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
pos = 0
time = 0
vel = 0

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

screen.fill(BLACK)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                vel = -1
            if event.key == pygame.K_RIGHT:
                vel = 1
        elif event.type == pygame.KEYUP:
            vel = 0
    pos += vel
    pygame.draw.line(screen, WHITE, (pos,time), (pos,time))
    pygame.display.flip()
    time += 1
