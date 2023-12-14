import pygame
class Trap(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, width, height):
        super().__init__()
        self.original_image = pygame.image.load(".\My_game\Assets\_trap.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (width,height))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x, pos_y)
        self.angle = 0  # Ángulo de rotación

    def update(self):
        # Rotar la imagen
        self.angle = (self.angle - 1) % 360  # Aumentar el ángulo (puedes ajustar la velocidad de rotación)
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)