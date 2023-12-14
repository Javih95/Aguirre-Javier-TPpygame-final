import pygame
import random
class Vida(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, width, height):
        super().__init__()
        self.image = pygame.image.load(".\My_game\Assets\corazon.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (width,height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x, pos_y)
class Frutas(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, width, height):
        super().__init__()
        lista_de_imagenes = [".\My_game\Assets\Apple.png",".\My_game\Assets\Bananas.png",".\My_game\Assets\Cherries.png"]
        selected_image = random.choice(lista_de_imagenes)
        self.image = pygame.image.load(selected_image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width,height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x, pos_y)
class Check_point(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, width, height):
        super().__init__()
        self.image = pygame.image.load(".\My_game\Assets\checkpoint.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (width,height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x, pos_y)
class Trofeo(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, width, height):
        super().__init__()
        self.image = pygame.image.load(".\My_game\Assets\_trofeo.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (width,height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x, pos_y)