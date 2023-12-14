import pygame
import pygame as pg
import random
from bala import Bala_enemigo
from raycast import Ray
from  auxiliar import SurfaceManager as sf
class Enemigo(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y,screen_w,screen_h):
        super().__init__()
        self.__walk_r = sf.get_surface_from_spritesheet(".\My_game\Assets\enemigo.png", 4, 1)
        self.__walk_l = sf.get_surface_from_spritesheet(".\My_game\Assets\enemigo.png", 4, 1,flip=True)
        self.__initial_frame = 0
        self.__actual_animation = self.__walk_r
        self.__frame_rate = 60
        self.__player_animation_time = 0
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        self.__is_looking_right = False
        self.quieto = True
        self.rect = self.__actual_img_animation.get_rect()
        self.ancho_rect = 80  # Ajusta el ancho deseado
        self.alto_rect = 70
        self.rect = pg.Rect(self.rect.x, self.rect.y, self.ancho_rect, self.alto_rect)
        #ROJO = (255, 0, 0)
        #self.image = pygame.Surface((50, 50))
        #self.image.fill(ROJO)
        #self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x, pos_y)
        self.en_suelo = False
        self.velocidad = 3
        self.direccion_move = random.choice([-1, 1])
        self.direccion = "derecha"
        self.shoot_timer = 0
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.detector_izq= detector_suelo(self.rect.x-40,self.rect.y+60)
        self.detector_der= detector_suelo(self.rect.x+40,self.rect.y+60)
        self.hay_suelo = False
        self.hay_suelo_izq = False
    def update(self,terrenos,plataformas,balas_1,jugador,plataforma_movil,screen,trampas,delta_ms):
        self.shoot_timer += 1
        if self.en_suelo:
            self.move()
        self.limitar()
        self. gravedad(terrenos,plataformas,plataforma_movil)
        self.mirar(jugador,balas_1)
        #self.detector_izq.dibujar(screen)
        self.detector_izq.update(self.rect.y+60,self.rect.x-20)
        #self.detector_der.dibujar(screen)
        self.detector_der.update(self.rect.y+60,self.rect.x+40)
        self.detectar_suelo(terrenos,plataformas,trampas)
        self.do_animation(delta_ms)
        self.run(self.direccion_move)
    def gravedad(self,terrenos,plataformas,plataforma_movil):
        colision_terreno = pg.sprite.spritecollide(self, terrenos, False)
        colision_plataforma = pg.sprite.spritecollide(self, plataformas, False)
        colision_plataforma_movil = pg.sprite.spritecollide(self, plataforma_movil, False)
        if not colision_terreno and not colision_plataforma and not colision_plataforma_movil :
            #self.rect.y += 1  # Aplicar gravedad
            self.en_suelo = False
        if colision_terreno:
            for terreno in colision_terreno:
                self.en_suelo = True
        if colision_plataforma and not colision_terreno:
            for plataforma in colision_plataforma:
                
                if(self.rect.bottom < plataforma.rect.top+3):  # Ajustar valor de tolerancia
                    self.en_suelo = True
                    self.en_plataforma= True
        if colision_plataforma_movil:
            for plataforma_movil in colision_plataforma_movil:
                if self.rect.bottom <= plataforma_movil.rect.top+3:  # Ajustar valor de tolerancia
                    self.en_suelo = True
                    #plataforma_movil = colision_plataforma_movil[0]
                    self.rect.x += plataforma_movil.movimiento
        if not self.en_suelo:
            self.rect.y += 2# Aplicar gravedad
    def move(self):
        self.rect.x += self.velocidad * self.direccion_move
        if self.direccion_move == -1:
            self.direccion = "izquierda"
        elif self.direccion_move == 1:
            self.direccion = "derecha"
        if not self.hay_suelo:
            self.direccion_move = -1
        if not self.hay_suelo_izq:
            self.direccion_move = 1
    def limitar(self):
        if self.rect.y >= self.screen_h:
            self.rect.y = self.screen_h
            self.en_suelo = True
        if self.rect.x < 10:
            self.direccion_move *= -1  # Cambia la dirección
        elif self.rect.x > self.screen_w-50:
            self.direccion_move *= -1  # Cambia la dirección
    def shoot(self, balas_1):
        if self.shoot_timer >= 20:
            bala = Bala_enemigo(self.rect.x + self.rect.width//2, self.rect.y, self.direccion_move,8)
            balas_1.add(bala)
            self.shoot_timer = 0
    def mirar(self,jugador,balas_1):
        ray = Ray(self.rect.center, pygame.Vector2(self.direccion_move, 0))  # Rayo apuntando hacia la derecha
        ray.advance(100)
        if ray.raycast([jugador]):
            self.shoot(balas_1)
    def detectar_suelo(self,terrenos,plataformas,trampas):
        colision_terreno_detector = pygame.sprite.spritecollide(self.detector_izq, terrenos, False)
        colision_plataforma_detector = pygame.sprite.spritecollide(self.detector_izq, plataformas, False)
        colision_terreno_detector_der= pygame.sprite.spritecollide(self.detector_der, terrenos, False)
        colision_plataforma_detector_der= pygame.sprite.spritecollide(self.detector_der, plataformas, False)
        colision_trampa_detector= pygame.sprite.spritecollide(self.detector_izq, trampas, False)
        colision_trampa_detector_der= pygame.sprite.spritecollide(self.detector_der, trampas, False)
        if colision_terreno_detector or colision_plataforma_detector:
            self.hay_suelo_izq= True
        if not colision_terreno_detector and not colision_plataforma_detector:
            self.hay_suelo_izq = False
        if colision_terreno_detector_der or colision_plataforma_detector_der:
            self.hay_suelo = True
        if not colision_terreno_detector_der and not colision_plataforma_detector_der:
            self.hay_suelo = False
        if  colision_trampa_detector_der:
            self.hay_suelo = False
        if colision_trampa_detector:
            self.hay_suelo_izq = False
    def __set_x_animations_preset(self, animation_list: list[pg.surface.Surface], look_r: bool):
        self.__actual_animation = animation_list
        self.__is_looking_right = look_r    
    def __set_y_animations_preset(self):
        #self.__move_y = -self.__jump
        self.__move_x = self.velocidad if self.__is_looking_right else -self.velocidad
        self.__actual_animation = self.__jump_r if self.__is_looking_right else self.__jump_l
        self.__initial_frame = 0
        #self.__is_jumping = True
    def run(self, direction):
            match direction:
                case -1:
                    look_right = True
                    self.__set_x_animations_preset(self.__walk_r, look_r=look_right)
                    if self.__initial_frame >= len(self.__walk_r)-1:
                        self.__initial_frame = 0
                case 1:
                    look_right = False
                    self.__set_x_animations_preset(self.__walk_l, look_r=look_right)
                    if self.__initial_frame >= len(self.__walk_l)-1:
                        self.__initial_frame = 0
    def do_animation(self, delta_ms):
        self.__player_animation_time += delta_ms
        if self.__player_animation_time >= self.__frame_rate:
            self.__player_animation_time = 0
            if self.__initial_frame < len(self.__actual_animation) - 1:
                self.__initial_frame += 1
            else:
                self.__initial_frame = 0
    def dibujar(self, screen: pg.surface.Surface):
        #pg.draw.rect(screen, 'red', self.rect)
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        self.image = pygame.transform.scale(self.__actual_img_animation, (100,100))
        #screen.blit(self.__actual_img_animation, ((self.rect.x),self.rect.y))
        screen.blit(self.image, ((self.rect.x-10),self.rect.y-20))
        #pg.draw.rect(screen, 'red', self.rect)
        #screen.blit(self.image, ((self.rect.x - 45),self.rect.y))
class detector_suelo():
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.ROJO = (0, 255, 0)
        self.image = pygame.Surface((10, 10))
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x, pos_y)
        self.pos_y = pos_y
        self.pos_x = pos_x
    def update(self,y,x):
        self.rect.y = y
        self.rect.x = x
    def dibujar(self, pantalla):
        pantalla.fill(self.ROJO, self.rect)   
class Enemigo_2(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y,screen_w,screen_h):
        super().__init__()
        self.__walk_r = sf.get_surface_from_spritesheet(".\My_game\Assets\enemigo2.png", 7, 1)
        self.__walk_l = sf.get_surface_from_spritesheet(".\My_game\Assets\enemigo2.png", 7, 1,flip=True)
        self.__initial_frame = 0
        self.__actual_animation = self.__walk_r
        self.__frame_rate = 60
        self.__player_animation_time = 0
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        self.__is_looking_right = False
        self.quieto = True
        self.rect = self.__actual_img_animation.get_rect()
        self.ancho_rect = 80  # Ajusta el ancho deseado
        self.alto_rect = 70
        self.rect = pg.Rect(self.rect.x, self.rect.y, self.ancho_rect, self.alto_rect)
        #ROJO = (255, 0, 0)
        #self.image = pygame.Surface((50, 50))
        #self.image.fill(ROJO)
        #self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x, pos_y)
        self.en_suelo = False
        self.velocidad = 3
        self.direccion_move = random.choice([-1, 1])
        self.direccion = "derecha"
        self.shoot_timer = 0
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.detector_izq= detector_suelo(self.rect.x-20,self.rect.y+60)
        self.detector_der= detector_suelo(self.rect.x+40,self.rect.y+60)
        self.hay_suelo = False
        self.hay_suelo_izq = False
    def update(self,terrenos,plataformas,balas_1,jugador,plataforma_movil,screen,trampas,delta_ms):
        self.shoot_timer += 1
        if self.en_suelo:
            self.move()
        self.limitar()
        self. gravedad(terrenos,plataformas,plataforma_movil)
        self.mirar(jugador,balas_1)
        #self.detector_izq.dibujar(screen)
        self.detector_izq.update(self.rect.y+60,self.rect.x-20)
        #self.detector_der.dibujar(screen)
        self.detector_der.update(self.rect.y+60,self.rect.x+40)
        self.detectar_suelo(terrenos,plataformas,trampas)
        self.do_animation(delta_ms)
        self.run(self.direccion_move)
    def gravedad(self,terrenos,plataformas,plataforma_movil):
        colision_terreno = pg.sprite.spritecollide(self, terrenos, False)
        colision_plataforma = pg.sprite.spritecollide(self, plataformas, False)
        colision_plataforma_movil = pg.sprite.spritecollide(self, plataforma_movil, False)
        if not colision_terreno and not colision_plataforma and not colision_plataforma_movil :
            #self.rect.y += 1  # Aplicar gravedad
            self.en_suelo = False
        if colision_terreno:
            for terreno in colision_terreno:
                self.en_suelo = True
        if colision_plataforma and not colision_terreno:
            for plataforma in colision_plataforma:
                
                if(self.rect.bottom < plataforma.rect.top+3):  # Ajustar valor de tolerancia
                    self.en_suelo = True
                    self.en_plataforma= True
        if colision_plataforma_movil:
            for plataforma_movil in colision_plataforma_movil:
                if self.rect.bottom <= plataforma_movil.rect.top+3:  # Ajustar valor de tolerancia
                    self.en_suelo = True
                    #plataforma_movil = colision_plataforma_movil[0]
                    self.rect.x += plataforma_movil.movimiento
        if not self.en_suelo:
            self.rect.y += 2# Aplicar gravedad
    def move(self):
        self.rect.x += self.velocidad * self.direccion_move
        if self.direccion_move == -1:
            self.direccion = "izquierda"
        elif self.direccion_move == 1:
            self.direccion = "derecha"
        if not self.hay_suelo:
            self.direccion_move = -1
        if not self.hay_suelo_izq:
            self.direccion_move = 1
    def limitar(self):
        if self.rect.y >= self.screen_h:
            self.rect.y = self.screen_h
            self.en_suelo = True
        if self.rect.x < 10:
            self.direccion_move *= -1  # Cambia la dirección
        elif self.rect.x > self.screen_w-50:
            self.direccion_move *= -1  # Cambia la dirección
    def shoot(self, balas_1):
        if self.shoot_timer >= 20:
            bala = Bala_enemigo(self.rect.x + self.rect.width//2, self.rect.y, self.direccion_move,8)
            balas_1.add(bala)
            self.shoot_timer = 0
    def mirar(self,jugador,balas_1):
        ray = Ray(self.rect.center, pygame.Vector2(self.direccion_move, 0))  # Rayo apuntando hacia la derecha
        ray.advance(200)
        if ray.raycast([jugador]):
            self.velocidad *= 2
        else:
            self.velocidad =3
    def detectar_suelo(self,terrenos,plataformas,trampas):
        colision_terreno_detector = pygame.sprite.spritecollide(self.detector_izq, terrenos, False)
        colision_plataforma_detector = pygame.sprite.spritecollide(self.detector_izq, plataformas, False)
        colision_terreno_detector_der= pygame.sprite.spritecollide(self.detector_der, terrenos, False)
        colision_plataforma_detector_der= pygame.sprite.spritecollide(self.detector_der, plataformas, False)
        colision_trampa_detector= pygame.sprite.spritecollide(self.detector_izq, trampas, False)
        colision_trampa_detector_der= pygame.sprite.spritecollide(self.detector_der, trampas, False)
        if colision_terreno_detector or colision_plataforma_detector:
            self.hay_suelo_izq= True
        if not colision_terreno_detector and not colision_plataforma_detector:
            self.hay_suelo_izq = False
        if colision_terreno_detector_der or colision_plataforma_detector_der:
            self.hay_suelo = True
        if not colision_terreno_detector_der and not colision_plataforma_detector_der:
            self.hay_suelo = False
        if  colision_trampa_detector_der:
            self.hay_suelo = False
        if colision_trampa_detector:
            self.hay_suelo_izq = False
    def __set_x_animations_preset(self, animation_list: list[pg.surface.Surface], look_r: bool):
        self.__actual_animation = animation_list
        self.__is_looking_right = look_r    
    def __set_y_animations_preset(self):
        #self.__move_y = -self.__jump
        self.__move_x = self.velocidad if self.__is_looking_right else -self.velocidad
        self.__actual_animation = self.__jump_r if self.__is_looking_right else self.__jump_l
        self.__initial_frame = 0
        #self.__is_jumping = True
    def run(self, direction):
            match direction:
                case -1:
                    look_right = True
                    self.__set_x_animations_preset(self.__walk_r, look_r=look_right)
                    if self.__initial_frame >= len(self.__walk_r)-1:
                        self.__initial_frame = 0
                case 1:
                    look_right = False
                    self.__set_x_animations_preset(self.__walk_l, look_r=look_right)
                    if self.__initial_frame >= len(self.__walk_l)-1:
                        self.__initial_frame = 0
    def do_animation(self, delta_ms):
        self.__player_animation_time += delta_ms
        if self.__player_animation_time >= self.__frame_rate:
            self.__player_animation_time = 0
            if self.__initial_frame < len(self.__actual_animation) - 1:
                self.__initial_frame += 1
            else:
                self.__initial_frame = 0
    def dibujar(self, screen: pg.surface.Surface):
        #pg.draw.rect(screen, 'red', self.rect)
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        self.image = pygame.transform.scale(self.__actual_img_animation, (100,100))
        screen.blit(self.image, ((self.rect.x-10),self.rect.y-30))
        #pg.draw.rect(screen, 'red', self.rect)        
class Enemigo_estatico(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y,direccion,rango):
        super().__init__()
        self.__idle_r = sf.get_surface_from_spritesheet(".\My_game\Assets\enemigoestatico.png", 8, 1)
        self.__idle_l = sf.get_surface_from_spritesheet(".\My_game\Assets\enemigoestatico.png", 8, 1,flip=True)
        self.__atack_r = sf.get_surface_from_spritesheet(".\My_game\Assets\enemigoestatico.png", 8, 1)
        self.__atack_l = sf.get_surface_from_spritesheet(".\My_game\Assets\enemigoestatico.png", 8, 1,flip=True)

        self.__initial_frame = 0
        self.__actual_animation = self.__idle_r
        self.__frame_rate = 60
        self.__player_animation_time = 0
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        self.__is_looking_right = False
        self.quieto = True
        self.rect = self.__actual_img_animation.get_rect()
        self.ancho_rect = 80  # Ajusta el ancho deseado
        self.alto_rect = 70
        self.rect = pg.Rect(self.rect.x, self.rect.y, self.ancho_rect, self.alto_rect)
        #self.image = pygame.Surface((50, 50))
        #self.image.fill((50,60,39))
        #self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x, pos_y)
        self.direccion = direccion
        self.rango = rango
        self.shoot_timer = 0
        self.disparando = False
    def update(self,terrenos,plataformas,balas_1,jugador,plataforma_movil,screen,trampas,delta_ms):
        self.shoot_timer += 1
        self.mirar(jugador,balas_1)
        self.do_animation(delta_ms)
        self.direccion_animacion(self.direccion)
    def shoot(self, balas_1):
        if self.shoot_timer >= 20:
            bala = Bala_enemigo(self.rect.x + self.rect.width//2, self.rect.y, self.direccion,8)
            balas_1.add(bala)
            self.shoot_timer = 0
            print("bang")
    def mirar(self,jugador,balas_1):
        ray = Ray(self.rect.center, pygame.Vector2(self.direccion, 0))  # Rayo apuntando hacia la derecha
        ray.advance(self.rango)
        if ray.raycast([jugador]):
            self.shoot(balas_1)
            self.disparando = True
            self.quieto= False
        else:
            self.quieto=True
            self.disparando=False
            
    def __set_x_animations_preset(self, animation_list: list[pg.surface.Surface], look_r: bool):
        self.__actual_animation = animation_list
        self.__is_looking_right = look_r    
    def __set_y_animations_preset(self):
        #self.__move_y = -self.__jump
        self.__move_x = self.velocidad if self.__is_looking_right else -self.velocidad
        self.__actual_animation = self.__jump_r if self.__is_looking_right else self.__jump_l
        self.__initial_frame = 0
        #self.__is_jumping = True
    def direccion_animacion(self, direction):
            match direction:
                case -1:
                    if self.quieto:
                        look_right = True
                        self.__set_x_animations_preset(self.__idle_r, look_r=look_right)
                        if self.__initial_frame >= len(self.__idle_r)-1:
                            self.__initial_frame = 0
                    if self.disparando:
                         look_right = True
                         self.__set_x_animations_preset(self.__atack_r, look_r=look_right)
                         if self.__initial_frame >= len(self.__atack_r)-1:
                            self.__initial_frame = 0

                case 1:
                    if self.quieto:
                        look_right = False
                        self.__set_x_animations_preset(self.__idle_l, look_r=look_right)
                        if self.__initial_frame >= len(self.__idle_l)-1:
                            self.__initial_frame = 0
                        if self.disparando:
                         self.__set_x_animations_preset(self.__atack_l, look_r=look_right)
                         if self.__initial_frame >= len(self.__atack_l)-1:
                            self.__initial_frame = 0

    def do_animation(self, delta_ms):
        self.__player_animation_time += delta_ms
        if self.__player_animation_time >= self.__frame_rate:
            self.__player_animation_time = 0
            if self.__initial_frame < len(self.__actual_animation) - 1:
                self.__initial_frame += 1
            else:
                self.__initial_frame = 0
    def dibujar(self, screen: pg.surface.Surface):
        #pg.draw.rect(screen, 'red', self.rect)
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        self.image = pygame.transform.scale(self.__actual_img_animation, (100,100))
        screen.blit(self.image, ((self.rect.x-10),self.rect.y-30))
        #pg.draw.rect(screen, 'red', self.rect)