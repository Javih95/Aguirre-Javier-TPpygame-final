import pygame
class Terreno(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, width, height):
        super().__init__()
        original_image = pygame.image.load(".\My_game\Assets\piso.png")
        self.image = pygame.transform.scale(original_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x, pos_y)
