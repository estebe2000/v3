import pygame, os.path,pytmx, pyscroll, sys, platform, datetime
from setting import *
from effects import *
from fx_rain import *
from fx_fire import *
from fx_light import *
from dialog import *
import xml.etree.ElementTree as ET
from dataclasses import dataclass

pygame.init()
clock = pygame.time.Clock()
now = datetime.datetime.now()

# Create the window, saving it to a variable.
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jeu NSI")

def ma_musique_de_fond(choix_musique):
    # definir la musique
    pygame.mixer.init()
    PATH = './sounds/' + choix_musique + '.mp3'
    if not (os.path.isfile(PATH) and os.access(PATH, os.R_OK)):
        PATH = './sounds/default.mp3'
    pygame.mixer.music.load(PATH)
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)  # If the loops is -1 then the music will repeat indefinitely.

def newxw(current_screen,n):
    return int(n / screen_width * current_screen.get_width())

def newyh(current_screen,n):
    return int(n / screen_height * current_screen.get_height())

def newzoom(current_screen,n):
    return float(float(n) / screen_width * current_screen.get_width())

def son_short(name):
    pas = pygame.mixer.Sound(f'./sounds/{name}.mp3')
    pygame.mixer.Sound.set_volume(pas, 0.5)
    pas.play(0)