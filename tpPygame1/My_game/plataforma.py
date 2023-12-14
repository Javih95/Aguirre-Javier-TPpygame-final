from typing import Any
import pygame
import pygame as pg
from  auxiliar import SurfaceManager as sf
class Plataforma(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, width, height):
        super().__init__()
        original_image = pygame.image.load(".\My_game\Assets\plataforma.png")
        self.image = pygame.transform.scale(original_image, (width, height))
        #self.image = pygame.Surface((width, height))
        #self.image.fill((128, 128, 128))
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x, pos_y)
class Plataforma_movil(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, width, height,speed,rango,direccion):
        super().__init__()
        original_image = pygame.image.load(".\My_game\Assets\plataformamovil.png")
        self.image = pygame.transform.scale(original_image, (width, height))
        #self.image = pygame.Surface((width, height))
        #self.image.fill((128, 128, 128))
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x, pos_y)
        self.pos_x = pos_x
        self.velocidad = speed
        self.direccion_move = direccion
        self.movimiento= self.velocidad * self.direccion_move
        self.rango = rango
    def update(self):
        self.movimiento= self.velocidad * self.direccion_move
        self.rect.x += self.movimiento
        if self.rect.x <= self.pos_x-self.rango:
            self.rect.x = self.pos_x - self.rango
            self.direccion_move *= -1  # Cambia la dirección
        elif self.rect.x >= self.pos_x + self.rango:
            self.rect.x = self.pos_x + self.rango
            self.direccion_move *= -1  # Cambia la dirección
class Plataforma_trampa(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((128, 128, 128))
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x, pos_y)
        self.pos_y = pos_y
        self.caer = False
        self.se_cayo = False
        self.espera_timer = 0
    def update(self):
        self.caer()
        self.subir()
    def caer(self):
        if self.caer:
            self.espera_timer += 1
            if self.espera_timer >= 180:
                self.rect.y += 5
                self.espera_timer = 0
                self.caer = False
                self.se_cayo = True
    def subir(self):
        if self.se_cayo:
            self.espera_timer +=1
            if self.espera_timer >= 300:
                if self.rect.y >= 660:
                    self.rect.y += 1
                    self.se_cayo = False
                if self.y == self.pos_y:
                    self.rect.y = self.pos_y 
                    self.se_cayo = False
