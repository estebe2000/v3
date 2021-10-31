import pygame
from random import randint, choice
from math import cos, sin

j = 0
particles = list()
#screen = pygame.display.set_mode((800, 600))



class Particle_fire:
    def __init__(self, x=315, y=500, sliders=(3, 1, 0.4, 1, 0), res=1, screen=pygame.display.set_mode((800, 600))):
        self.x, self.y = x, y
        self.maxlife = randint(13 + int(sliders[0] * 5), 27 + int(sliders[0] * 10))
        self.life = self.maxlife
        self.dir = choice((-2, -1, 1, 2))
        self.sin = randint(-10, 10) / 7
        self.sinr = randint(5, 10)
        self.r = randint(0, 2)
        self.sliders = sliders
        self.ox = randint(-1, 1)
        self.oy = randint(-1, 1)
        self.res = res
        self.screen = screen
        self.bsurf = pygame.Surface((screen.get_width(), screen.get_height()))
        self.bsurf.set_colorkey((0, 0, 0))



    def particle_list(self) -> list:
        "Create a list of particles"
        for d in range(0, int(10), 10):
            _x = self.x + cos(10) * d
            _y = self.y + sin(10) * d
            for _ in range(round(self.sliders[1])): particles.append(Particle_fire(_x // self.res, _y // self.res))
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
            p.life -= 1
            if p.life == 0: dead.append(p); continue

            i = int((p.life / p.maxlife) * 6)

            p.y -= self.sliders[2]
            p.x += ((p.sin * sin(j / (p.sinr))) / 2) * self.sliders[3] + self.sliders[4]

            if not randint(0, 5): p.r += 0.88

            x, y = p.x, p.y

            x += p.ox * (5 - i)
            y += p.oy * (5 - i)

            alpha = 255
            if p.life < p.maxlife / 4:
                alpha = int((p.life/p.maxlife)*255)

            pygame.draw.circle(self.bsurf, palette[i] + (alpha,), (x, y), p.r, 0)

            if i == 0:
                pygame.draw.circle(self.bsurf, (0, 0, 0, 0), (x + randint(-1, 1), y - 4),
                                   p.r * (((p.maxlife - p.life) / p.maxlife) / 0.88), 0)

            else:
                pygame.draw.circle(self.bsurf, palette[i - 1] + (alpha,), (x + randint(-1, 1), y - 3), p.r / 1.5, 0)

        for p in dead:
            particles.remove(p)
        dead.clear()
        self.screen.blit(pygame.transform.scale(self.bsurf, (self.screen.get_width() * self.res, self.screen.get_height() * self.res)), (0, 0))

