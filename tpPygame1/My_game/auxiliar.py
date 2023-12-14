import pygame
import sys
from tkinter import simpledialog
import numpy as np
class Cronometro:
    def __init__(self, tiempo_inicial_segundos):
        self.tiempo_inicial = tiempo_inicial_segundos
        self.tiempo_restante = tiempo_inicial_segundos*60
        self.font = pygame.font.Font(None, 36)
        self.texto = None
    def update(self):
        self.tiempo_restante -= 1
        if self.tiempo_restante < 0:
            self.tiempo_restante = 0
        self.texto = self.font.render(f"Tiempo: {self.tiempo_restante//60}", True, (255, 255, 255))
    def dibujar(self, pantalla):
        pantalla.blit(self.texto, (10, 10))
class Boton_nivel():
    def __init__(self,pos_x, pos_y,texto):
        original_image = pygame.image.load(".\My_game\Assets\Boton_nivel_bloqueado.png")
        self.image = pygame.transform.scale(original_image, (200, 200))
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)
        self.texto_color = (128, 128, 128)
        self.font = pygame.font.Font(None, 36)
        self.texto_obtenido=texto
        self.texto_constructor(self.texto_obtenido)
    def texto_constructor(self,texto):
        self.texto = self.font.render(texto, True, self.texto_color)
        self.texto_rect = self.texto.get_rect()
        self.texto_rect.center = self.rect.center
    def dibujar(self, pantalla):
        pantalla.blit(self.image, self.rect)
        pantalla.blit(self.texto,self.texto_rect)
    def chequear_click(self,mouse_pos):
        return self.rect.collidepoint(mouse_pos)
class Boton():
    def __init__(self,pos_x, pos_y,texto):
        original_image = pygame.image.load(".\My_game\Assets\_boton_textura.png")
        self.image = pygame.transform.scale(original_image, (200, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)
        self.texto_color = (128, 128, 128)
        self.font = pygame.font.Font(None, 36)
        self.texto_constructor(texto)
    def texto_constructor(self,texto):
        self.texto = self.font.render(texto, True, self.texto_color)
        self.texto_rect = self.texto.get_rect()
        self.texto_rect.center = self.rect.center
    def dibujar(self, pantalla):
        pantalla.blit(self.image, self.rect)
        pantalla.blit(self.texto,self.texto_rect)
    def chequear_click(self,mouse_pos):
        return self.rect.collidepoint(mouse_pos)
    """
class Boton():
    def __init__(self,pos_x, pos_y,texto):
        self.color = (255, 0, 0)
        self.rect = pygame.Rect(0,0,200,50)
        self.rect.center = (pos_x, pos_y)
        self.texto_color = (128, 128, 128)
        self.font = pygame.font.Font(None, 36)
        self.texto_constructor(texto)
    def texto_constructor(self,texto):
        self.texto = self.font.render(texto, True, self.texto_color,self.color)
        self.texto_rect = self.texto.get_rect()
        self.texto_rect.center = self.rect.center
    def dibujar(self, pantalla):
        pantalla.fill(self.color, self.rect)
        pantalla.blit(self.texto,self.texto_rect)
    def chequear_click(self,mouse_pos):
        return self.rect.collidepoint(mouse_pos)
        """
class Deslizador():
    def __init__(self, x, y, width, height):
        original_image = pygame.image.load(".\My_game\Assets\_boton_textura.png")
        self.image = pygame.transform.scale(original_image, (width, height))
        self.rect = self.image.get_rect()
        #self.rect = pygame.Rect(x, y, width, height)
        self.rect.center=(x, y)
        #self.color = (0,0, 0)
        self.seleccionado = False
        self.initial_x = x-width/2
    def dibujar(self, screen):
        screen.blit(self.image, self.rect)
        #pygame.draw.rect(screen, self.color, self.rect)
    def chequear_click(self,mouse_pos):
        return self.rect.collidepoint(mouse_pos)
class barra_deslizador():
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.rect.center=(x, y)
        self.color = (0,0, 0)
    def dibujar(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, width=1)
class Indicador_volumen():
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.rect.topleft=(x, y)
        self.color = (255,0, 0)
    def dibujar(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
class Input_text:
    def __init__(self, pos_x, pos_y):
        self.color = (100, 50, 180)
        self.rect = pygame.Rect(0, 0, 200, 50)
        self.rect.center = (pos_x, pos_y)
        self.texto_color = (128, 128, 128)
        self.font = pygame.font.Font(None, 36)
        self.texto = ""
        self.texto_renderizado = None
    def renderizar_texto(self):
        self.texto_renderizado = self.font.render(self.texto, True, self.texto_color, self.color)
        self.texto_rect = self.texto_renderizado.get_rect()
        self.texto_rect.center = self.rect.center

    def dibujar(self, pantalla):
        if self.texto_renderizado is None:
            self.renderizar_texto()
        pantalla.fill(self.color, self.rect)
        pantalla.blit(self.texto_renderizado, self.texto_rect)
    def obtener_nombre(self):
        return simpledialog.askstring("Ingresar Nombre", "Por favor, ingresa tu nombre")
    def update(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN:
                self.texto = self.obtener_nombre()
                # Abre un cuadro de diálogo para ingresar el nombre
                print("Nombre ingresado:", self.texto)
            elif evento.key == pygame.K_BACKSPACE:
                if len(self.texto) > 0:
                    self.texto = self.texto[:-1]
            else:
                self.texto += evento.unicode
            self.texto_renderizado= None
        return self.texto
    def chequear_click(self,mouse_pos):
        return self.rect.collidepoint(mouse_pos)
class Titulo():
    def __init__(self,pos_x, pos_y):
        original_image = pygame.image.load(".\My_game\Assets\_titulo.png")
        self.image = pygame.transform.scale(original_image, (600, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)
    def dibujar(self, pantalla):
        pantalla.blit(self.image, self.rect)
class SurfaceManager:
    @staticmethod
    def get_surface_from_spritesheet(img_path: str, cols: int, rows: int, step = 1, flip: bool = False) -> list[pygame.surface.Surface]:
        sprites_list = list()
        surface_img = pygame.image.load(img_path)
        frame_width = int(surface_img.get_width()/cols)
        frame_height = int(surface_img.get_height()/rows)

        for row in range(rows):

            for column in range(0, cols, step):
                x_axis = column * frame_width
                y_axis = row * frame_height

                frame_surface = surface_img.subsurface(
                    x_axis, y_axis, frame_width, frame_height
                )

                if flip:
                    frame_surface = pygame.transform.flip(frame_surface, True, False)
                sprites_list.append(frame_surface)
        return sprites_list
def map_value(value, in_min, in_max, out_min, out_max):
    return np.interp(value, [in_min, in_max], [out_min, out_max])