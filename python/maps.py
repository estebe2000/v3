from player import *


@dataclass
class Portal:
    from_world: str
    origin_point: str
    target_world: str
    teleport_point: str


@dataclass
class Map:
    name: str
    walls: list[pygame.Rect]
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals: list[Portal]
    npcs: list[NPC]
    key2cont: str
    meteo: str
    feu: list[pygame.Rect]
    bulle: list[pygame.Rect]
    clef: list[pygame.Rect]
    zoom: float


class MapManager:

    def __init__(self, screen, player, language):
        self.maps = dict()
        self.screen = screen
        self.player = player
        self.current_map = ljeu
        ma_musique_de_fond(self.current_map)
        self.language = language

        self.register_maps()

        self.teleport_player("player")
        self.teleport_npc()

        self.keyok = False
        self.recup_cle = False

        self.info_key = False
        self.logo = pygame.image.load("./medias/loupe.png")
        self.icon_clef1 = pygame.image.load("./medias/key_1.png")
        self.logo2 = pygame.image.load("./medias/key_2.png")


    def check_npc_collision(self, dialog_box):

        for sprite in self.get_group().sprites():
            if sprite.feet.colliderect(self.player.rect) and type(sprite) is NPC:
                fin = dialog_box.execute(sprite.dialog)
                sprite.talking()

                if sprite.is_name() == self.key2continus and fin:
                    self.keyok = True
                    self.logo = pygame.image.load("./medias/loupe1.png")
            if sprite.feet.colliderect(self.player.rect) and type(sprite) is Leskey:
                self.recup_cle = True

    def check_key_collection(self, dialog_box, info=[]):

        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)
                if self.player.feet.colliderect(rect) and not (self.keyok) and not (self.info_key):
                    dialog_box.execute(info)
                    self.info_key = True
                elif self.player.feet.colliderect(rect) and not (self.keyok) and self.info_key:
                    dialog_box.next_text()
                    self.info_key = False

    def check_collisions(self):
        # portails
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)

                if self.player.feet.colliderect(rect) and self.keyok and self.recup_cle:
                    copy_portal = portal
                    self.current_map = portal.target_world
                    self.teleport_player(copy_portal.teleport_point)
                    # lancer font sonore
                    ma_musique_de_fond(self.current_map)

        # collision
        for sprite in self.get_group().sprites():

            if type(sprite) is NPC:
                if sprite.feet.colliderect(self.player.rect):
                    sprite.speed = 0
                else:
                    sprite.speed = 1

            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()

            if not self.get_clef() or sprite.feet.collidelist(self.get_clef()) > -1:
                self.icon_clef1 = pygame.image.load("./medias/key_2.png")
                self.logo2 = pygame.image.load("./medias/key_1.png")
                #self.recup_cle = True

    def teleport_player(self, name):

        self.icon_clef1 = pygame.image.load("./medias/key_1.png")
        self.logo2 = pygame.image.load("./medias/key_2.png")
        if self.get_key() == 'None':
            self.keyok = True
            self.logo = pygame.image.load("./medias/loupe1.png")
        else:
            self.key2continus = self.get_key()
            self.keyok = False
            self.logo = pygame.image.load("./medias/loupe.png")

        self.recup_cle = False

        self.listes_cjefs = self.loc_clef()
        print(self.listes_cjefs)
        for clefs in self.listes_cjefs:
            pass
            a = Leskey(x=clefs.x/self.get_zoom(), y=clefs.y/self.get_zoom())
            a.change_animation("down")

            self.get_group().add(a)

        point = self.get_object(name)

        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()


    def register_maps(self):
        doc = ET.parse('./setting/maps.xml')

        # pour toutes les maps dans le xml
        for AAA in doc.findall('map'):
            portals = []
            npcs = []
            nbport = (len(AAA.findall('portal')))
            npnpc = (len(AAA.findall('npc')))
            name = AAA[0].text
            key = AAA[1].text
            meteo = AAA[2].text
            zoom = newzoom(self.screen,AAA[3].text)
            # print(f"La map {name} a {nbport} portails et {npnpc} PNJ")

            # Charger la carte
            tmx_data = pytmx.util_pygame.load_pygame(f"./maps/tmx/{name}.tmx")
            map_data = pyscroll.data.TiledMapData(tmx_data)
            map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
            map_layer.zoom = newzoom(self.screen,AAA[3].text)

            # Les collisions
            walls = []
            # les feux
            feu = []
            # les bulles
            bulle = []
            # les clefs
            clef = []

            # Dessiner les différents calques
            group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
            group.add(self.player)

            for obj in tmx_data.objects:
                if obj.type == "collision":
                    walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
                if obj.type == "feu":
                    feu.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
                if obj.type == "bulle":
                    bulle.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
                if obj.type == "clef":
                    clef.append(pygame.Rect(obj.x, obj.y, 16, 32))

            # ajout des portails
            for port in range(nbport):
                portals.append(Portal(from_world=f'{AAA[4 + port][0].text}', origin_point=f'{AAA[4 + port][1].text}',
                                      target_world=f'{AAA[4 + port][2].text}',
                                      teleport_point=f'{AAA[4 + port][3].text}'))
            # ajout des npcs
            for pnj in range(npnpc):
                new_dial = []
                nom_pnj = AAA[4 + nbport + pnj][0].text
                nbpoint = int(AAA[4 + nbport + pnj][1].text)
                dial_pnj = f"[{AAA[4 + nbport + pnj][2].text}]"
                if dial_pnj != '[None]':
                    txt_dial = str(dial_pnj).split(",")
                    for txt in range(len(txt_dial)):
                        new_dial.append(txt_dial[txt].replace("[", "").replace("]", "").replace("'", ""))

                npcs.append(NPC(nom_pnj, nb_points=nbpoint, dialog=new_dial, lang=(self.get_language())))

            # recuperer tous les npcs pour les ajouter au groupe
            for npc in npcs:
                group.add(npc)


            # Creer un objet map
            self.maps[name] = Map(name, walls, group, tmx_data, portals, npcs, key, meteo, feu, bulle, clef, zoom)

    def get_map(self):
        return self.maps[self.current_map]

    def get_group(self):
        return self.get_map().group

    def get_key(self):
        return str(self.get_map().key2cont)

    def get_walls(self):
        return self.get_map().walls

    def get_feu(self):
        return self.get_map().feu

    def get_bulle(self):
        return self.get_map().bulle

    def get_clef(self):
        return self.get_map().clef

    def loc_feu(self):
        # les feux
        feux = []

        for obj in self.get_map().tmx_data.objects:
            if obj.type == "feu":
                feux.append(pygame.Rect(obj.x * self.get_zoom(), obj.y * self.get_zoom(), obj.width, obj.height))
        return feux

    def loc_bulle(self):
        # les bulles
        bulles = []

        for obj in self.get_map().tmx_data.objects:
            if obj.type == "bulle":
                bulles.append(pygame.Rect(obj.x * self.get_zoom(), obj.y * self.get_zoom(), obj.width, obj.height))
        return bulles

    def loc_clef(self):
        # les bulles
        clefs = []

        for obj in self.get_map().tmx_data.objects:
            if obj.type == "clef":
                clefs.append(pygame.Rect(obj.x * self.get_zoom(), obj.y * self.get_zoom(), obj.width, obj.height))

        return clefs

    def get_language(self):
        return self.language

    def get_meteo(self):
        return str(self.get_map().meteo)

    def get_zoom(self):
        return self.get_map().zoom

    def get_object(self, name):
        return self.get_map().tmx_data.get_object_by_name(name)

    def teleport_npc(self):
        for map in self.maps:
            map_data = self.maps[map]
            npcs = map_data.npcs

            for npc in npcs:
                npc.load_points(map_data.tmx_data)
                npc.teleport_spawn()

    def draw(self):

        self.get_group().draw(self.screen)
        self.screen.set_colorkey((0, 0, 0))
        blur(self.screen, (0, 0), (800, 45), 1)
        myfont = pygame.font.Font("./dialogs/dialog_font.ttf", 18)
        now2 = datetime.datetime.now()
        dif = str(now2 - now)
        nowstr = now2.strftime("%Y-%m-%d %H:%M:%S")
        date = myfont.render(nowstr, 1, (255, 255, 0))
        self.screen.blit(date, (10, 10))
        score_display = myfont.render(dif, 1, (255, 255, 0))
        self.screen.blit(score_display, (300, 10))
        key = self.get_key()
        self.screen.blit(self.logo, (740, 20))
        self.screen.blit(self.logo2, (710, 20))
        self.get_group().center(self.player.rect.center)


        for feux in self.loc_feu():
            pass
            if self.keyok:
                Particle_fire(feux.x, feux.y, res=2, screen=self.screen).show_particle()
        for bulles in self.loc_bulle():
            pass
            Particle_light(bulles.x, bulles.y, screen=self.screen, rgb=(0, 0, 0), rad=2, vit=5, haut=1).show_particle()
        for clefs in self.loc_clef() :
            #self.screen.blit(self.icon_clef1, (clefs.x, clefs.y))
            pass

        if self.get_meteo() == "pluis":
            Particle_rain(y=0, vit=5, screen=self.screen).show_particle()
        elif self.get_meteo() == "neige":
            Particle_rain(y=0, vit=1, screen=self.screen).show_particle()
        elif self.get_meteo() == "flou":
            blur(self.screen, (0, 0), (800, 600), 1)
        elif self.get_meteo() == "superflou":
            blur(self.screen, (0, 0), (800, 600), 3)

    def update(self):

        self.get_group().update()
        self.check_collisions()

        for npc in self.get_map().npcs:
            npc.move()
