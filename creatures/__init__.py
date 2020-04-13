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
        self.type = 'bacterium'
    def get_speed(self):
        self.speed = 13-self.mass + self.speed_boost

class Virus:
    def __init__(self, pos, endurance=40, speed_boost=0, color=(0, 225, 0)):
        self.mass = 1
        self.speed = 10-self.mass
        self.pos  = pos
        self.last_eat = 0
        self.endurance = endurance
        self.speed_boost = speed_boost
        self.color = color
        self.type = 'virus'
    def get_speed(self):
        self.speed = 13-self.mass + self.speed_boost


class Creatures(object):
    def __init__(self, win, win_yx):
        self.win = win
        self.bacteriums = []
        self.viruses = []
        self.eat = []
        self.win_yx = win_yx

    def draw(self):
        for bacterium in self.bacteriums:
            # print(creature.pos)
            pygame.draw.circle(self.win, bacterium.color, bacterium.pos[:2], bacterium.mass)
        for virus in self.viruses:
            pygame.draw.circle(self.win, virus.color, virus.pos[:2], virus.mass)
        for pos_ in self.eat:
            if pos_[2] == 'poison':
                pygame.draw.circle(self.win, (0, 100, 225), pos_[:2], 5)
            else:
                pygame.draw.circle(self.win, (225, 225, 225), pos_[:2], 5)
        pygame.draw.rect(self.win, (0, 225, 0), (0, 0, 180, 80))
        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface = myfont.render("Bacteriums: %s" % (len(self.bacteriums)), True, (225, 225, 225))
        self.win.blit(textsurface, (20,20))
        textsurface = myfont.render("Viruses: %s" % (len(self.viruses)), True, (225, 225, 225))
        self.win.blit(textsurface, (20, 50))




    def die(self):
        for bacterium in self.bacteriums + self.viruses:
            if bacterium.last_eat + bacterium.endurance < 3:
                if bacterium.type == 'virus':
                    self.viruses.remove(bacterium)
                elif bacterium.type == 'bacterium':
                    self.bacteriums.remove(bacterium)
            else:
                bacterium.last_eat -= 5
    def move(self):
        for bacterium in self.bacteriums + self.viruses:
            distance = []
            eat_ = []
            if bacterium.type == 'virus':
                for pos_ in self.bacteriums + self.eat:
                    # print(bacterium)
                    try:
                        width = bacterium.pos[0] - pos_[0]
                        heidth = bacterium.pos[1] - pos_[1]
                        distance.append(round(sqrt(width**2 + heidth**2)))
                        eat_.append([pos_[0], pos_[1], pos_[2]])
                    except TypeError:
                        width = bacterium.pos[0] - pos_.pos[0]
                        heidth = bacterium.pos[1] - pos_.pos[1]
                        distance.append(round(sqrt(width**2 + heidth**2)))
                        eat_.append([pos_.pos[0], pos_.pos[1], 'bacterium'])
            elif bacterium.type == 'bacterium':
                for pos_ in self.eat:
                    # print(bacterium.pos[0])
                    try:
                        width = abs(bacterium.pos[0] - pos_[0])
                        heidth = abs(bacterium.pos[1] - pos_[1])
                        distance.append(round(sqrt(width**2 + heidth**2)))
                        eat_.append([pos_[0], pos_[1], pos_[2]])
                    except TypeError:
                        pass
            if distance:
                min_d = min(distance)
                pos_eat = eat_[distance.index(min_d)]
                pos_creat = bacterium.pos
                if (pos_creat[0] - pos_eat[0]) == 0:
                    alfa = atan((pos_creat[1] - pos_eat[1]) / 0.0000001)
                else:
                    alfa = atan((pos_creat[1] - pos_eat[1]) / (pos_creat[0] - pos_eat[0]))
                if pos_eat[0] <= pos_creat[0]:
                    alfa = pi+alfa

                if bacterium.speed < min_d:
                    pos_creat[0] = round(pos_creat[0] + cos(alfa)*bacterium.speed)
                    pos_creat[1] = round(pos_creat[1] + sin(alfa)*bacterium.speed)
                else:
                    pos_creat[0] = round(pos_creat[0] + cos(alfa)*min_d)
                    pos_creat[1] = round(pos_creat[1] + sin(alfa)*min_d)


                if bacterium.mass == 10:
                    if bacterium.type == 'virus':
                        self.add(bacterium.pos, True)
                    else:
                        self.add(bacterium.pos)
                    bacterium.mass = 1
                    bacterium.get_speed()

                if pos_creat == pos_eat[:2]:
                    if eat_[distance.index(min_d)][2] == 'poison':
                        if bacterium.type == 'virus':
                            self.viruses.remove(bacterium)
                        else:
                            self.bacteriums.remove(bacterium)
                        self.eat.remove(eat_[distance.index(min_d)])
                    else:
                        try:
                            self.eat.remove(pos_eat)
                        except:
                            # print(self.bacteriums, pos_eat[3])
                            self.bacteriums.remove(self.del_bacterium(pos_eat[:2]))
                        bacterium.mass += 1
                        bacterium.get_speed()
                        bacterium.last_eat += 1


    def del_bacterium(self, pos):
        for bacterium in self.bacteriums:
            if bacterium.pos == pos:
                return bacterium
        return 0

    def add(self, pos=[50, 100], virus=False):
        if not random.randint(0, 40) or virus:
            self.viruses.append(Virus([pos[0] + 10, pos[1] + 10]))
        elif random.randint(0, 4):
            self.bacteriums.append(Bacterium([pos[0] + 10, pos[1] + 10]))
        else:
            self.bacteriums.append(Bacterium([pos[0] + 10, pos[1] + 10], random.randint(0, 4), random.randint(0, 10), (225, 0, 0)))

    def add_eat(self):
        win_x = self.win_yx[0]
        win_y = self.win_yx[1]
        if random.randint(0, 40):
            self.eat.append([random.randint(0, win_x), random.randint(0, win_y), "eat"])
        else:
            self.eat.append([random.randint(0, win_x), random.randint(0, win_y), "poison"])