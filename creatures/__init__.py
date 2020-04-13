import pygame
import random
from math import sqrt, pi, atan, sin, cos

class Bacterium:
    def __init__(self, pos, endurance=0, speed_boost=0, color=(225, 0, 225)):
        self.mass = 1
        self.speed = 10-self.mass
        self.pos  = pos
        self.last_eat = 0
        self.endurance = endurance
        self.speed_boost = speed_boost
        self.color = color
    def get_speed(self):
        self.speed = 13-self.mass + self.speed_boost

class Creatures(object):
    def __init__(self, win, win_yx):
        self.win = win
        self.bacteriums = []
        self.eat = []
        self.win_yx = win_yx

    def draw(self):
        for creature in self.bacteriums:
            # print(creature.pos)
            pygame.draw.circle(self.win, creature.color, creature.pos[:2], creature.mass)
        for pos_ in self.eat:
            if pos_[2] == 'poison':
                pygame.draw.circle(self.win, (225, 225, 0), pos_[:2], 5)
            else:
                pygame.draw.circle(self.win, (225, 225, 225), pos_[:2], 5)

        pygame.draw.rect(self.win, (0, 225, 0), (0, 0, 180, 50))
        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface = myfont.render("Bacteriums: %s" % (len(self.bacteriums)), True, (225, 225, 225))
        self.win.blit(textsurface, (20,20))

    def die(self):
        for creature in self.bacteriums:
            if creature.last_eat + creature.endurance < 5:
                self.bacteriums.remove(creature)
            else:
                creature.last_eat = 0
    def move(self):
        for creature in self.bacteriums:
            distance = []
            eat_ = []
            for pos_ in self.eat:
                width = abs(creature.pos[0] - pos_[0])
                heidth = abs(creature.pos[1] - pos_[1])
                distance.append(round(sqrt(width**2 + heidth**2)))
                eat_.append([pos_[0], pos_[1], pos_[2]])
            if distance:
                min_d = min(distance)
                pos_eat = eat_[distance.index(min_d)]
                pos_creat = creature.pos
                if (pos_creat[0] - pos_eat[0]) == 0:
                    alfa = atan((pos_creat[1] - pos_eat[1]) / 0.0000001)
                else:
                    alfa = atan((pos_creat[1] - pos_eat[1]) / (pos_creat[0] - pos_eat[0]))
                if pos_eat[0] <= pos_creat[0]:
                    alfa = pi+alfa

                if creature.speed < min_d:
                    pos_creat[0] = round(pos_creat[0] + cos(alfa)*creature.speed)
                    pos_creat[1] = round(pos_creat[1] + sin(alfa)*creature.speed)
                else:
                    pos_creat[0] = round(pos_creat[0] + cos(alfa)*min_d)
                    pos_creat[1] = round(pos_creat[1] + sin(alfa)*min_d)


                if creature.mass == 10:
                    self.add(creature.pos)
                    creature.mass = 1
                    creature.get_speed()

                if pos_creat == pos_eat[:2]:
                    if eat_[distance.index(min_d)][2] == 'poison':
                        self.bacteriums.remove(creature)
                        self.eat.remove(eat_[distance.index(min_d)])
                    else:
                        self.eat.remove(pos_eat)
                        creature.mass += 1
                        creature.get_speed()
                        creature.last_eat += 1
            # else:
            #     self.creatures = []
            #     # break

    def add(self, pos=[50, 100]):
        if random.randint(0, 4):
            self.bacteriums.append(Bacterium([pos[0] + 10, pos[1] + 10]))
        else:
            self.bacteriums.append(Bacterium([pos[0] + 10, pos[1] + 10], random.randint(0, 4), random.randint(0, 10), (225, 0, 0)))

    def add_eat(self):
        win_x = self.win_yx[0]
        win_y = self.win_yx[1]
        if random.randint(0, 20):
            self.eat.append([random.randint(0, win_x), random.randint(0, win_y), "eat"])
        else:
            self.eat.append([random.randint(0, win_x), random.randint(0, win_y), "poison"])