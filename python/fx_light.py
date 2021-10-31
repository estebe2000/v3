import pygame, sys, random


particles = []


def circle_surf(radius, color):
    surf = pygame.Surface((radius * 2, radius * 2))
    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey((0, 0, 0))
    return surf

class Particle_light:
    def __init__(self, x=0, y=10,vit=10,rad=1,rgb=(0,0,0),haut=3,screen=pygame.display.set_mode((800, 600))):
        self.x, self.y = x, y
        self.vit = vit
        self.rad = rad
        self.rgb = rgb
        self.haut= haut
        self.screen = screen
        self.bsurf = pygame.Surface((screen.get_width(), screen.get_height()))
        self.bsurf.set_colorkey((0, 0, 0))



    def show_particle(self):
        #self.bsurf.fill((0, 0, 0))
        particles.append([[self.x, self.y], [random.randint(0, 20) / 10 - 1, -5], random.randint(6, 11)])

        for particle in particles:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 0.1
            particle[1][1] += 0.45 / self.haut
            pygame.draw.circle(self.bsurf, (255, 255, 255), [int(particle[0][0]), int(particle[0][1])], int(particle[2])/5*self.rad)

            radius = particle[2] /5*self.rad
            self.bsurf.blit(circle_surf(radius, (self.rgb)), (int(particle[0][0] - radius), int(particle[0][1] - radius)))

            if particle[2] <= 50 / self.vit:
                particles.remove(particle)



        self.screen.blit(self.bsurf, (0, 0))

