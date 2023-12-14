import pygame
import sys
import random
from gameManagercopy import *
from enemy import *
# Define una clase para el generador de enemigos
class EnemyGenerator:
    def __init__(self,screen_w,screen_h):
        self.enemies = pygame.sprite.Group()
        self.spawn_timer = 0
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.enigo_estatico =False
        self.cantidad=3
    def update(self,level,screen,terrenos,plataformas,balas_1,player,plataforma_movil,trap,enemigo_uno,enemigo_dos,enemigo_tres,delta_ms):
    # Actualiza el temporizador y genera enemigos si es necesario
        self.spawn_timer += 1
        if self.spawn_timer >= 60 and len(self.enemies) < self.cantidad:  # Genera un enemigo cada segundo (60 fotogramas)
            self.spawn_enemy(level,enemigo_uno,enemigo_dos,enemigo_tres)
            self.spawn_timer = 0
        for enemy in self.enemies:
            enemy.dibujar(screen)
            enemy.update(terrenos,plataformas,balas_1,player,plataforma_movil,screen,trap,delta_ms)
    def spawn_enemy(self,level,enemigo_uno,enemigo_dos,enemigo_tres):
        if level == "1":
            enemy = Enemigo(random.randint(0, 1200), 0,self.screen_w,self.screen_h)
            self.enemies.add(enemy)
            self.cantidad=3
        elif level == "2":
            enemy_2 = Enemigo_2(random.randint(0, 1200), 0,self.screen_w,self.screen_h)
            self.enemies.add(enemy_2)
            self.cantidad=3
        elif level == "3":
            enemy_2 = Enemigo_2(random.randint(0, 1200), 0,self.screen_w,self.screen_h)
            self.enemies.add(enemy_2)
            enemy = Enemigo(random.randint(0, 1200), 0,self.screen_w,self.screen_h)
            self.enemies.add(enemy)
            self.cantidad=3
            if not self.enigo_estatico:
                enemy_estatico = Enemigo_estatico(1000,350,-1,200)
                self.enemies.add(enemy_estatico)
                self.enigo_estatico=True
        elif level == "0":
            self.cantidad=1
            if not enemigo_uno:
                enemy = Enemigo(random.randint(0, 500), 0,self.screen_w,self.screen_h)
                self.enemies.add(enemy)
            if not enemigo_dos:
                enemy_2 = Enemigo_2(random.randint(500, 1000), 0,self.screen_w,self.screen_h)
                self.enemies.add(enemy_2)
            if not enemigo_tres:
                enemy_estatico = Enemigo_estatico(1000,570,-1,400)
                self.enemies.add(enemy_estatico)
    def eliminar_elementos(self):
        self.enemies.empty()