import pygame
import sys
from player import Player
from enemy import *
from ground import Terreno
from plataforma import *
from vidas import *
from enemyGenerator import EnemyGenerator
from trap import Trap
from auxiliar import *
from explosion import *
from menu import *
from ranking import *
from level import *
import json
class Game_1:
    def __init__(self,screen_w,screen_h):
        
        pygame.mixer.init()
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.level = None
        self.en_level = None
        #Player
        self.player = Player(300, 300,self.screen_w,self.screen_h)
        #self.players = pygame.sprite.Group()
        #self.players.add(self.player)
        self.balas = pygame.sprite.Group()
        self.bombas = pygame.sprite.Group()
        #Enemigo
        self.enemyGenerator = EnemyGenerator(self.screen_w,self.screen_h)
        self.balas_1 = pygame.sprite.Group()
        #cronometro
        self.cronometro = Cronometro(60)
        self.collision_clock =0
        #Vidas
        self.puntos = self.player.puntos
        self.cantidad_vidas = self.player.vidas
        self.font = pygame.font.Font(None, 36)
        #estados
        self.en_juego= False
        self.en_pausa= False
        self.ranking_menu = False
        self.game_over = False
        self.colision_jugador_enemigo_procesada = False
        self.sonido = True
        self.en_setting = False
        self.puede_pasar =False
        self.datos= Manejo_de_datos("lista_jugadores.json")
        self.enemigo_uno_muerto =False
        self.enemigo_dos_muerto=True
        self.enemigo_tres_muerto=True

        #sonidos
        self.sonido_reproducido = False
        self.colision_fruta_sound = pygame.mixer.Sound("./My_game/Assets/Sound/fruta.wav")
        self.colision_fruta_sound.set_volume(1)
        self.sonido_vida_reproducido = False
        self.colision_vida_sound = pygame.mixer.Sound("./My_game/Assets/Sound/vida.wav")
        self.colision_vida_sound.set_volume(1)
        self.sonido_checkpoint_reproducido = False
        self.colision_checkpoint_sound = pygame.mixer.Sound("./My_game/Assets/Sound/paso_de_nivel.wav")
        self.colision_checkpoint_sound.set_volume(1)
        self.daño_enemigo_sonido =pygame.mixer.Sound("./My_game/Assets/Sound/daño_enemigo.wav")
        self.daño_enemigo_sonido_reproducido = False
        self.herida_sonido = pygame.mixer.Sound("./My_game/Assets/Sound/herida.wav")
        self.herida_sonido_reproducido =False
        self.trofeo_sonido = pygame.mixer.Sound("./My_game/Assets/Sound/_trofeo.wav")
        self.trofeo_sonido_reproducido = False
        self.lista_de_canciones = ["./My_game/Assets/Sound/fondo1.mp3","./My_game/Assets/Sound/fondo2.ogg","./My_game/Assets/Sound/fondo3.ogg"] 
        self.cancion_elegida = self.lista_de_canciones[0]
        self.sonido_fondo =pygame.mixer.Sound(self.cancion_elegida)
        pygame.mixer.music.load(self.cancion_elegida)
        #pygame.mixer.music.play(-1)
        #Menu
        self.menu_pausa = Menu_pausa(screen_w/2,screen_h/2,screen_w,screen_h)
        self.ranking = Ranking(screen_w/2,screen_h/2,400,400,self.datos.lista_jugadores)
        self.menu_settings = Settings(screen_w/2,screen_h/2,screen_w,screen_h)
    def load_level(self, level_name):
        if self.level is not None:
            self.level.eliminar_elementos()
            self.enemyGenerator.eliminar_elementos()
        with open(".\My_game\levels.json") as json_file:
            data = json.load(json_file)
        for level_data in data["levels"]:
            if level_data["name"] == level_name:
                self.level = Level(self.screen_w, self.screen_h, level_data)
                self.en_level = self.level.en_level
                break
        self.definir_sonido_fondo()
        pygame.mixer.music.play(-1)
    def run(self,teclas,screen,delta_ms,volumen_musica):
        if self.en_juego and not self.game_over:
                if not self.en_pausa and not self.en_setting:
                    self.level.update(screen)
                    self.ranking_menu = False
                    self.collision_clock += 1
                    self.puntos = self.player.puntos
                    self.cantidad_vidas = self.player.vidas
                    self.player.update(self.balas,self.bombas,teclas,self.level.terrenos, self.level.plataformas,self.level.plataforma_movil,delta_ms,self.sonido)
                    self.balas.update()
                    self.balas_1.update()
                    self.bombas.update()
                    self.level.trap.update()
                    self.enemyGenerator.update(self.en_level,screen,self.level.terrenos,self.level.plataformas,self.balas_1,self.player,self.level.plataforma_movil,self.level.trap,self.enemigo_uno_muerto,self.enemigo_dos_muerto,self.enemigo_tres_muerto,delta_ms)
                    self.cronometro.update()
                    if self.cronometro.tiempo_restante <= 0 :
                            self.game_over= True
                self.musica_fondo_control(volumen_musica)
                self.player.dibujar(screen)
                self.balas.draw(screen)
                self.balas_1.draw(screen)
                self.bombas.draw(screen)
                self.cronometro.dibujar(screen)
                self.dañar_jugador()
                self.dañar_enmigo()
                self.sumar_vidas()
                self.sumar_puntos()
                self.daño_trampa()
                self.control_check_point()
                self.chequear_puede_pasar()
                self.puntos_texto = self.font.render(f"Puntos: {self.puntos}", True, (255, 255, 255))
                self.vidas_texto = self.font.render(f"Vidas: {self.cantidad_vidas}", True, (255, 255, 255))
                screen.blit(self.vidas_texto, (10,50))
                screen.blit(self.puntos_texto, (10,30))
                if self.en_pausa:
                    self.menu_pausa.dibujar(screen)
                    if self.ranking_menu:
                        self.ranking.dibujar(screen)
                self.game_over_fun(screen)
        if self.game_over:
            self.ranking.dibujar(screen)
            pygame.mixer.music.stop()
    def dañar_enmigo(self):
        colisiones_balas = pygame.sprite.groupcollide(self.enemyGenerator.enemies, self.balas, True, True)
        colisiones_bombas = pygame.sprite.groupcollide(self.enemyGenerator.enemies, self.bombas, True, False)
        colisiones = {**colisiones_balas,**colisiones_bombas}
        for enemigo_dañado in colisiones.keys():
            self.player.puntos +=100
            if self.en_level=="0":
                if not self.enemigo_uno_muerto:
                    self.enemigo_uno_muerto =True
                    self.enemigo_dos_muerto=False
                elif not self.enemigo_dos_muerto:
                    self.enemigo_dos_muerto=True
                    self.enemigo_tres_muerto =False
                elif not self.enemigo_tres_muerto:
                    self.enemigo_tres_muerto=True
            if self.sonido:
                if not self.daño_enemigo_sonido_reproducido:
                    self.daño_enemigo_sonido.play()
                    self.daño_enemigo_sonido_reproducido =True
                self.daño_enemigo_sonido_reproducido=False
    def dañar_jugador(self):
            if not self.colision_jugador_enemigo_procesada:
                colisiones_jugador_enemigos = pygame.sprite.spritecollide(self.player, self.enemyGenerator.enemies, False)
                for colision in colisiones_jugador_enemigos:
                    print ("te dieron")
                    self.player.vidas -=1
                    #print(self.player.vidas)
                    self.colision_jugador_enemigo_procesada = True
                    self.collision_clock=0
                    if self.sonido:
                        if not self.herida_sonido_reproducido:
                            self.herida_sonido.play()
                            self.herida_sonido_reproducido = True
                        self.herida_sonido_reproducido=False
            if self.collision_clock >= 300:
                self.colision_jugador_enemigo_procesada = False
                colisiones_balas = pygame.sprite.spritecollide(self.player,self.balas_1,False)
                for colision in  colisiones_balas:
                    #print ("te dieron")
                    self.player.vidas -=1
                    #print(self.player.vidas)
                    self.colision_jugador_enemigo_procesada = True
                    self.collision_clock=0
                    if self.sonido:
                       if not self.herida_sonido_reproducido:
                           self.herida_sonido.play()
                           self.herida_sonido_reproducido = True
                       self.herida_sonido_reproducido=False
            if self.collision_clock >= 300:
                self.colision_jugador_enemigo_procesada = False
    def sumar_vidas(self):
        colisiones_vidas = pygame.sprite.spritecollide(self.player, self.level.vidas, True)
        for colision in colisiones_vidas:
            self.player.vidas +=1
            if self.sonido:
                if not self.sonido_vida_reproducido:
                    self.colision_vida_sound.play()
                    self.sonido_vida_reproducido = True
                self.sonido_vida_reproducido = False
    def sumar_puntos(self):
        colisiones_frutas = pygame.sprite.spritecollide(self.player, self.level.frutas,True)
        for colision in colisiones_frutas:
            self.player.puntos +=10
            if self.sonido:
                if not self.sonido_reproducido:
                    self.colision_fruta_sound.play()
                    self.sonido_reproducido = True
                self.sonido_reproducido = False
    def daño_trampa(self):
        colision_trampa= pygame.sprite.spritecollide(self.player, self.level.trap, False)
        for colision in colision_trampa:
            if not self.colision_jugador_enemigo_procesada:
                self.player.vidas -=1
                self.colision_jugador_enemigo_procesada = True
                self.collision_clock=0
            if self.sonido:
                        if not self.herida_sonido_reproducido:
                            self.herida_sonido.play()
                            self.herida_sonido_reproducido = True
                        self.herida_sonido_reproducido=False
            if self.player.direccion_move == 1:
                self.player.rect.x = self.player.rect.x-10
            elif self.player.direccion_move == -1:
                self.player.rect.x = self.player.rect.x +10
        if self.collision_clock >= 600:
            self.colision_jugador_enemigo_procesada = False
    def control_check_point(self):
        colisiones_check_point = pygame.sprite.spritecollide(self.player, self.level.checkpoint,False)
        for colision in colisiones_check_point:
            if self.puede_pasar:
                if self.sonido:
                    if not self.sonido_checkpoint_reproducido:
                        self.colision_checkpoint_sound.play()
                        self.sonido_checkpoint_reproducido = True
                    self.sonido_checkpoint_reproducido = False
                if self.en_level ==  "1":
                    self.puede_pasar =False
                    self.sonido_fondo.stop()
                    self.player.rect.x = 100
                    self.player.rect.y = 500
                    self.cronometro.tiempo_restante = 60*60
                    self.load_level("Level2")
                elif self.en_level ==  "2":
                    self.puede_pasar =False
                    self.sonido_fondo.stop()
                    self.player.rect.x = 100
                    self.player.rect.y = 500
                    self.cronometro.tiempo_restante = 60*60
                    self.load_level("Level3")
                    self.en_level = self.level.en_level
                elif self.en_level ==  "3":
                    self.puede_pasar =False
                    self.sonido_fondo.stop()
                    self.game_over=True
                    #self.player.rect.x = 100
                    #self.player.rect.y = 500
                    #self.cronometro.tiempo_restante = 60*60
                    #self.load_level("Level1")
                    #self.en_level = self.level.en_level
                elif self.en_level ==  "0":
                     self.game_over = True 
                     self.cronometro.tiempo_restante = 60*60
                print ("Pasa de nivel")
    def chequear_puede_pasar(self):
        if len(self.level.frutas) <=0:
            colision_trofeo= pygame.sprite.spritecollide(self.player, self.level.trofeo,True)
            if colision_trofeo:
                self.puede_pasar = True
                if self.sonido:
                    if not self.trofeo_sonido_reproducido:
                        self.trofeo_sonido.play()
                        self.trofeo_sonido_reproducido = True
                    self.trefeo_sonido_reproducido=False
    def game_over_fun(self,screen):
        if self.player.vidas <= 0:
            self.datos.guardar_datos("lista_jugadores",self.player.puntos,self.player.nombre)
            self.game_over = True 
    def definir_sonido_fondo(self):
                    if self.en_level == "1":
                        self.cancion_elegida = self.lista_de_canciones[0]
                        #pygame.mixer.music.load(self.cancion_elegida)
                        self.sonido_fondo =pygame.mixer.Sound(self.cancion_elegida)
                        pygame.mixer.music.load(self.cancion_elegida)
                    if self.en_level == "2":
                        self.cancion_elegida = self.lista_de_canciones[1]
                        #pygame.mixer.music.load(self.cancion_elegida)
                        self.sonido_fondo =pygame.mixer.Sound(self.cancion_elegida)
                        pygame.mixer.music.load(self.cancion_elegida)
                    if self.en_level == "3":
                        self.cancion_elegida = self.lista_de_canciones[2]
                        #pygame.mixer.music.load(self.cancion_elegida)
                        self.sonido_fondo =pygame.mixer.Sound(self.cancion_elegida)
                        pygame.mixer.music.load(self.cancion_elegida)
    def musica_fondo_control(self,volumen_musica):
        if self.sonido:
            #pygame.mixer.music.play(-1)

            pygame.mixer.music.set_volume(volumen_musica)
           # self.sonido_fondo.set_volume(volumen_musica)
            #self.sonido_fondo.play()
            print(volumen_musica)
        if not self.sonido:
            pygame.mixer.music.set_volume(0)

