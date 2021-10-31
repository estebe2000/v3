import pygame
from random import randint, choice
from math import cos, sin
import random

j = 0
particles = list()



class Particle_rain:
    def __init__(self, x=0, y=10,vit=1, screen=pygame.display.set_mode((800, 600))):
        self.x, self.y = x, y
        self.vit = vit
        self.screen = screen
        self.bsurf = pygame.Surface((screen.get_width(), screen.get_height()))
        self.bsurf.set_colorkey((0, 0, 0))

    def particle_list(self) -> list:
        "Create a list of particles"
        _x = random.randint(0, self.screen.get_width())
        _y = self.y
        for _ in range(1): particles.append(Particle_rain(_x, _y))
        return particles

    def show_particle(self):
        self.bsurf.fill((0, 0, 0))
        # you can change the palette
        palette = ((61, 38, 48),
                   (115, 61, 56),
                   (191, 74, 46),
                   (247, 117, 33),
                   (255, 173, 51),
                   (255, 255, 0))
        dead = list()
        particles = self.particle_list()

        for p in particles:
            if p.y >= self.screen.get_width(): dead.append(p); continue

            p.y -= -self.vit
            p.x -= 0
            x, y = p.x, p.y

            pygame.draw.circle(self.bsurf, (255, 255, 255), (x, y), 1, 0)

        for p in dead:
            particles.remove(p)
        dead.clear()
        self.screen.blit(self.bsurf, (0, 0))

