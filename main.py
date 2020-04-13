import pygame
import random

from creatures import Bacterium, Creatures


########################
print('MADE BY drogi17')
########################


speed = 0
win_x = 1000
win_y = 1000

pygame.init()
win = pygame.display.set_mode((win_x, win_y))   # отображение окна
pygame.display.set_caption("v1")                # заголовок окна

cursor = pygame.mouse.get_pos
run = True

things = Creatures(win, [win_x, win_y])
things.add([random.randint(0, win_x), random.randint(0, win_y-100)])
things.add([random.randint(0, win_x), random.randint(0, win_y-100)])
for _ in range(1000):
    things.eat.append([random.randint(0, win_x), random.randint(0, win_y), "eat"])

for _ in range(1):
    things.eat.append([random.randint(0, win_x), random.randint(0, win_y), "poison"])


evant_time = 0

while run:
    win.fill((0, 0, 0))
    pygame.time.delay(int(speed))
    for event in pygame.event.get():    #quit
        if event.type == pygame.QUIT:   #quit
            run = False                 #quit

    things.move()
    things.draw()
    if evant_time == 40:
        things.die()
        evant_time = 0
    if evant_time in range(30):
        things.add_eat()
    evant_time += 1
    pygame.display.update()