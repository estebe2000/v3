
tile_size = 32
screen_width = 800
screen_height = 576

# fichier menu
fmenu = "../textes/menu.txt"

# liste pour le menu
items = []
texts, langs = [], []
# couleur Menu
color = (255, 255, 255)
color_light = (0, 200, 0)
color_dark = (100, 100, 100)
# Visual menu
image_fd = "fond.png"
logo_fd = "logo-nsi.png"
# musique menu
mmenu = "story"

colonne_menu = ((len(open(fmenu).readlines())//4)+1)

# map de lancement du jeu
ljeu = "story"

# skin du joueur
sjoueur = "player"

