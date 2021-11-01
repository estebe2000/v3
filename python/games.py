from maps import *


def maj_screen():

    pygame.display.update()


class Game:

    def __init__(self):
        self.running = True
        # Affichage de la fenêtre
        self.screen = screen

        self.groupeGlobal = pygame.sprite.Group()

        # Générer le joeur
        self.player = Player()
        self.dialog_box = DialogBox()



        # Définir le logo du jeu
        pygame.display.set_icon(self.player.image)

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_ESCAPE]:
            self.running = False
        elif pressed[pygame.K_UP]:
            self.player.move_up()
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()

    def update(self):
        self.map_manager.update()

    def menu(self):
        image_fond = pygame.image.load(f"../medias/{image_fd}")
        logo_fond = pygame.image.load(f"../medias/{logo_fd}")
        ma_musique_de_fond(mmenu)

        with open(fmenu) as f:
            for line in f:
                line = line.replace('"', '').strip()
                items.append([line.split()[0], line.split()[1]])
                # list languages
                langs.append(line.split()[1])

        while True:
            font_size = newyh(self.screen,25)
            smallfont = pygame.font.SysFont('Corbel', font_size)
            texts = []
            for item in items:
                texts.append(smallfont.render(item[0], True, color))
            image_fond = pygame.transform.scale(image_fond, (self.screen.get_width(), self.screen.get_height()))
            logo_fond = pygame.transform.scale(logo_fond, (self.screen.get_width(), self.screen.get_height() // 5))
            self.screen.fill((255, 255, 255))
            self.screen.blit(image_fond, (0, 0))
            self.screen.blit(logo_fond, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                if event.type == pygame.VIDEORESIZE:
                    old_surface_saved = self.screen
                    self.screen = pygame.display.set_mode((event.w, event.h),
                                                          pygame.RESIZABLE)
                    self.screen.blit(old_surface_saved, (0, 0))

                    del old_surface_saved

            mouse = pygame.mouse.get_pos()
            for i in range(len(items)):
                hauteur = (i // colonne_menu) + 1
                collone = (i % colonne_menu)
                x_col = (self.screen.get_width() / (colonne_menu + 1))
                y_col = (self.screen.get_height() / 2)
                decal = (self.screen.get_width() / (colonne_menu + 1) * collone)
                if (x_col - newxw(self.screen,70)) + decal <= mouse[0] <= (
                        x_col + newxw(self.screen,70)) + decal and y_col - newyh(self.screen,100) + hauteur * newyh(self.screen,50) <= mouse[
                    1] <= y_col - newyh(self.screen,60) + hauteur * newyh(self.screen,50):
                    col = color_light
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.language = langs[i]
                        if self.language == 'ex':
                            pygame.quit()
                            sys.exit()
                        else:
                            self.run(self.language)

                else:
                    col = color_dark
                pygame.draw.rect(self.screen, col,
                                 [x_col - newxw(self.screen,70) + decal, y_col - newyh(self.screen,100) + hauteur * newyh(self.screen,50),
                                 newxw(self.screen,140), newyh(self.screen,40)])
                # superimposing the text onto our button
                self.screen.blit(texts[i],
                                 (x_col - newxw(self.screen,60) + (self.screen.get_width() / (colonne_menu + 1) * collone),
                                  (self.screen.get_height() / 2) - newyh(self.screen,90) + hauteur * newyh(self.screen,50)))

            # updates the frames of the game
            maj_screen()

    def run(self, language):
        clock = pygame.time.Clock()
        self.language = language
        self.map_manager = MapManager(self.screen, self.player, self.language)

        # Clock
        while self.running:

            self.player.save_location()
            self.handle_input()
            self.update()
            self.map_manager.draw()
            self.dialog_box.render(self.screen)
            caption = 'NSI JEUX -FPS: {} - Python {}  Pygame {} - Language {} '.format(int(clock.get_fps()),platform.python_version(),pygame.version.ver,self.language)
            pygame.display.set_caption(caption)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.map_manager.check_npc_collision(self.dialog_box,move=False)
                        self.map_manager.check_key_collection(self.dialog_box,["trop tot"])
                    else:
                        self.map_manager.check_npc_collision(self.dialog_box, move=True)
            clock.tick(60)

        pygame.quit()
        sys.exit()

    def _initialiser(self):
        try:
            self.ecran.detruire()
            # Suppression de tous les sprites du groupe
            self.groupeGlobal.empty()
        except AttributeError:
            pass