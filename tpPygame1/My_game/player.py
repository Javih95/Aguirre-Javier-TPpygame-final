import pygame as pg
import sys
from bala import *
from  auxiliar import SurfaceManager as sf
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y,screen_w,screen_h):
        super().__init__()
        pygame.mixer.init()
        self.disparo_sonido = pygame.mixer.Sound("./My_game/Assets/Sound/ataque.wav")
        self.disparo_sonido_reproducido =False
        self.bomba_sonido = pygame.mixer.Sound("./My_game/Assets/Sound/bomba.wav")
        self.bomba_sonido_reproducido =False
        self.limite_x = screen_w
        self.limite_y = screen_h
        #animacion
        self.__walk_r = sf.get_surface_from_spritesheet(".\My_game\Assets\lobofinal.png", 4, 1)
        self.__walk_l = sf.get_surface_from_spritesheet(".\My_game\Assets\lobofinal.png", 4, 1,flip=True)
        self.__iddle_r = sf.get_surface_from_spritesheet(".\My_game\Assets\lobofinalstay.png", 7, 1)
        self.__iddle_l = sf.get_surface_from_spritesheet(".\My_game\Assets\lobofinalstay.png", 7, 1,flip=True)
        self.__initial_frame = 0
        self.__actual_animation = self.__iddle_r
        self.__frame_rate = 60
        self.__player_animation_time = 0
        #self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        self.__is_looking_right = False
        self.quieto = True
        #self.image = pygame.transform.scale(self.__actual_img_animation, (15, 61))
        self.rect = self.__actual_img_animation.get_rect()
        self.ancho_rect = 30  # Ajusta el ancho deseado
        self.alto_rect = 123
        self.rect = pg.Rect(self.rect.x, self.rect.y, self.ancho_rect, self.alto_rect)
        self.rect.topleft = (pos_x, pos_y)
        #atributos
        self.vidas = 3
        self.puntos = 0
        self.nombre = ""
        self.velocidad = 5
        self.velocidad_salto = 130
        self.direccion_move = 1
        self.en_suelo = False
        self.en_plataforma= False
        self.en_plataforma_movil= False
        self.en_plataforma= False
        self.angulo_bomba = 45
        self.shoot_timer = 0
        self.speed_bala_y = 0
        self.gravedad_int = 0
        self.velocidad_saltando =0
        angulo_radianes = math.radians(45)
        velocidad_x = (self.velocidad_saltando*self.direccion_move)* math.cos(angulo_radianes)
        velocidad_y = -self.velocidad_saltando * math.sin(angulo_radianes)
        self.saltando = False
        self.puede_saltar = True
        self.ya_disparo=False
        self.ya_tiro_bomba=False
        self.ya_salto=False
# Velocidades iniciales
        self.velocidad_x = velocidad_x
        self.velocidad_y = velocidad_y
    def update(self,balas,bombas,teclas,terrenos, plataformas,plataforma_movil,delta_ms,sonido):
        self.shoot(balas,teclas,sonido)
        self.shoot_timer += 1
        self.limitar()
        self.move(teclas)
        self.shoot_bomba(teclas,bombas,sonido)
        self.muerte()
        self. gravedad(terrenos,plataformas,plataforma_movil)
        self.jump(teclas)
        """
        if self.saltando:
                    self.velocidad_y += self.gravedad_int
                    # Actualizar posición
                    self.rect.x += self.velocidad_x
                    self.rect.y += self.velocidad_y
        """
        self.do_animation(delta_ms)
        self.stay()
        self.run(self.direccion_move)
    def gravedad(self,terrenos,plataformas,plataforma_movil):
        colision_terreno = pg.sprite.spritecollide(self, terrenos, False)
        colision_plataforma = pg.sprite.spritecollide(self, plataformas, False)
        colision_plataforma_movil = pg.sprite.spritecollide(self, plataforma_movil, False)
        if not colision_terreno and not colision_plataforma and not colision_plataforma_movil :
            self.en_suelo = False
        if colision_terreno:
            for terreno in colision_terreno:
                self.en_suelo = True
                self.saltando =False
        if colision_plataforma and not colision_terreno:
            for plataforma in colision_plataforma:
                if(self.rect.bottom < plataforma.rect.top+7):  # Ajustar valor de tolerancia
                    self.en_suelo = True
                    self.en_plataforma= True
                    self.saltando =False
        else:
            self.en_plataforma=False
        if colision_plataforma_movil and not  self.en_plataforma :
            for plataforma_movil in colision_plataforma_movil:
                if self.rect.bottom <= plataforma_movil.rect.top + 3:
                #if self.rect.bottom <= plataforma_movil.rect.top+3:
                    self.en_suelo = True
                    self.saltando =False
                    self.rect.x += plataforma_movil.movimiento
        if not self.en_suelo:
           self.rect.y += 2 # Aplicar gravedad
    def move(self,teclas):
        if teclas[pg.K_LEFT]:
            self.rect.x -= self.velocidad
            self.direccion_move = -1
            self.speed_bala_y = 0
            self.angulo_bomba = 45
            self.__is_looking_right = False
            self.quieto=False
        if teclas[pg.K_RIGHT]:
            self.rect.x += self.velocidad
            self.direccion_move = 1
            self.speed_bala_y = 0
            self.angulo_bomba = 45
            self.__is_looking_right = True
            self.quieto=False
        if teclas[pg.K_UP]:
            self.direccion_move = 0
            self.angulo_bomba = 90
            self.speed_bala_y = 10
        if teclas[pg.K_DOWN]:
            self.direccion_move = 0
            self.angulo_bomba = 90
            self.speed_bala_y = -10
        if teclas[pg.K_UP] and teclas[pg.K_LEFT]:
            self.direccion_move = -1
            self.speed_bala_y = 10
        if teclas[pg.K_UP] and teclas[pg.K_RIGHT]:
            self.direccion_move = 1
            self.speed_bala_y = 10
        if teclas[pygame.K_DOWN] and teclas[pygame.K_LEFT]:
            self.direccion_move = -1
            self.speed_bala_y = -10
        if teclas[pg.K_DOWN] and teclas[pg.K_RIGHT]:
            self.direccion_move = 1
            self.speed_bala_y = -10
        if not teclas[pg.K_LEFT] and not teclas[pg.K_RIGHT]:
            self.quieto=True      
    def jump(self,teclas):
        """
        if teclas[pg.K_SPACE] and  not self.saltando:
                self.velocidad_saltando =18
                self.gravedad_int = 0.5
                angulo_radianes = math.radians(45)
                velocidad_x = (self.velocidad_saltando//2*self.direccion_move)* math.cos(angulo_radianes)
                velocidad_y = -self.velocidad_saltando * math.sin(angulo_radianes)
                self.velocidad_x = velocidad_x
                self.velocidad_y = velocidad_y
                self.saltando = True
        """
        if teclas[pg.K_SPACE]:
            if self.en_suelo:
                self.rect.y -= self.velocidad_salto
                #self.rect.x += self.velocidad_salto * self.direccion_move
                self.en_suelo = False   
                self.ya_salto=True
    def shoot(self, balas,teclas,sonido):
        # Crear una nueva bala en la posición del jugador y con la dirección actual
        if teclas[pg.K_s]:
            if self.shoot_timer >= 20:
                bala = Bala(self.rect.x + self.rect.width // 2,self.rect.y + self.rect.height // 2, self.direccion_move,10,self.speed_bala_y)
                balas.add(bala)
                self.shoot_timer = 0
                self.ya_disparo=True
                if sonido:
                    if not self.disparo_sonido_reproducido :
                        self.disparo_sonido.play()
                        self.disparo_sonido_reproducido=True
                    self.disparo_sonido_reproducido=False
    def shoot_bomba(self,teclas,bombas,sonido):
        if teclas[pygame.K_a]:
            if self.shoot_timer >= 20:
                bomba = Bomb(self.rect.x + self.rect.width // 2, self.rect.y,self.angulo_bomba,10,self.direccion_move)
                bombas.add(bomba)
                self.shoot_timer = 0
                self.ya_tiro_bomba=True
                if sonido:
                    if not self.bomba_sonido_reproducido :
                        self.bomba_sonido.play()
                        self.bomba_sonido_reproducido=True
                    self.bomba_sonido_reproducido=False
    def limitar(self):
        if self.rect.y >= self.limite_y - 10:
            self.vidas -=1
            self.rect.x = 100
            self.rect.y = 500
            #self.rect.y = self.limite_y -10
            self.en_suelo = True
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x >= self.limite_x -10:
            self.rect.x = self.limite_x -10
    def muerte(self):
        if self.vidas <= 0:
            print("has muerto")
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
        if not self.quieto:
            match direction:
                case 1:
                    look_right = True
                    self.__set_x_animations_preset(self.__walk_r, look_r=look_right)
                    if self.__initial_frame >= len(self.__walk_r)-1:
                        self.__initial_frame = 0
                case -1:
                    look_right = False
                    self.__set_x_animations_preset(self.__walk_l, look_r=look_right)
                    if self.__initial_frame >= len(self.__walk_l)-1:
                        self.__initial_frame = 0
    def stay(self):
        if self.quieto:
            if self.__actual_animation != self.__iddle_l and self.__actual_animation != self.__iddle_r:
                self.__actual_animation = self.__iddle_r if self.__is_looking_right else self.__iddle_l
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
        self.image = pygame.transform.scale(self.__actual_img_animation, (80, 80))
        screen.blit(self.__actual_img_animation, ((self.rect.x - 45),self.rect.y))
        #screen.blit(self.image, ((self.rect.x - 45),self.rect.y))
