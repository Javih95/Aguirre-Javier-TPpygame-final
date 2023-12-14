import pygame
from pygame.locals import *
from GUI_widget import *
import unicodedata

FPS = 60
#si creo un att del self en un metodo, eso impacta sobre la clase actual, o lo crea a nivel de la jerarquia de clases? por ej self.slave
#solo lo crea en button o en widget

    
class TextBox(Widget):
    def __init__(
            self, screen,master_x,master_y, x,y,w,h,
            color_background,color_background_seleccionado,color_border, color_border_seleccionado, border_size ,font, font_size,
            font_color):
        super().__init__(screen, x,y,w,h,color_background,color_border, border_size)
        
        pygame.font.init()#llamo al constructor de la fuente porque sino a veces pincha
        self._color_background_default = color_background
        self._color_border_default = color_border
        self._color_background_seleccionado = color_background_seleccionado
        self._color_border_seleccionado = color_border_seleccionado
        self.text = ""
        self._font = pygame.font.SysFont(font,font_size)
        self._font_color = font_color
        self._master_x = master_x
        self._master_y = master_y
        
        self.is_selected = False
        
        self.render()
        
    def get_text(self):
        return self.text    
    
    def set_text(self,texto):
        self.text = texto
        self.render()   
    
    def render(self):
        image_text = self._font.render(self.text, True, self._font_color, self._color_background)
        
        self._slave = pygame.surface.Surface((self._w,self._h))#superficie que se adapte a la del boton
        self.slave_rect = self._slave.get_rect()
        
        self.slave_rect.x = self._x
        self.slave_rect.y = self._y
        
        self.slave_rect_collide = pygame.Rect(self.slave_rect)
        self.slave_rect_collide.x += self._master_x
        self.slave_rect_collide.y += self._master_y
        
        
        self._slave.fill(self._color_background)
        
        media_texto_horizontal = image_text.get_width() / 2
        media_texto_vertical = image_text.get_height() / 2

        media_horizontal = self._w / 2
        media_vertical = self._h / 2
        diferencia_horizontal = media_horizontal - media_texto_horizontal 
        diferencia_vertical = media_vertical - media_texto_vertical
        
        self._slave.blit(image_text,(diferencia_horizontal,diferencia_vertical))#podriamos sacar cuentas para centrar el texto, por el momento 10-10
        
    def chequear_click(self,mouse_pos):
        return self.slave_rect.collidepoint(mouse_pos)
    def update(self):
        if self.is_selected:#me hicieron click, esto no siempre va a funcionar
                    self._color_background = self._color_background_seleccionado
                    self._color_border = self._color_border_seleccionado
        else:
            self._color_background = self._color_background_default
            self._color_border = self._color_border_default
            self.render()
        self.render()
        #self.draw()

        
         
