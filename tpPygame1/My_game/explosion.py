from typing import Any
import pygame 
import math
class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        # Agrega la lógica para la imagen de la explosión
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 255, 0))  # Color amarillo (puedes ajustarlo)
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x, pos_y)
        self.shockwaves = pygame.sprite.Group()
        print("bomba")
        # Crea sprites más pequeños que representan las ondas de choque
        self.create_shockwaves()
        

    def create_shockwaves(self):
        print("aaa")

        # Crea sprites más pequeños en diferentes direcciones
        for angle in range(0, 360, 45):
            shockwave = Shockwave(self.rect.x, self.rect.y, angle)
            self.shockwaves.add(shockwave)
        
    def update(self):
        print("bb")
        self.shockwaves.update()
class Shockwave(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, angle):
        super().__init__()
        # Agrega la lógica para la imagen de la onda de choque
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 0, 0))  # Color rojo (puedes ajustarlo)
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x, pos_y)

        # Convierte el ángulo a radianes
        angle_radians = math.radians(angle)
        # Asigna velocidades iniciales basadas en el ángulo
        self.speed_x = 5 * math.cos(angle_radians)
        self.speed_y = -5 * math.sin(angle_radians)

    def update(self):
        # Actualiza la posición de la onda de choque
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        print("ccc")