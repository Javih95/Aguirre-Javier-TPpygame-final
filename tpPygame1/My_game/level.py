import pygame
import sys
from ground import Terreno
from plataforma import *
from vidas import *
from trap import Trap
class Level:
    def __init__(self,screen_w,screen_h,level_data):
        self.fondo_img_path = level_data["fondo_img_path"]
        self.fondo_img = pygame.image.load(self.fondo_img_path).convert_alpha()
        self.fondo_img = pygame.transform.scale(self.fondo_img, (int(screen_w), int(screen_h)))

        self.terrenos = pygame.sprite.Group()
        self.plataformas = pygame.sprite.Group()
        self.plataforma_movil = pygame.sprite.Group()
        self.trap = pygame.sprite.Group()
        self.vidas = pygame.sprite.Group()
        self.frutas = pygame.sprite.Group()
        self.checkpoint =pygame.sprite.Group()
        self.trofeo = pygame.sprite.Group()
        self.en_level = level_data["en_level"]
        print(self.en_level)
        for terreno_data in level_data.get("terrenos", []):
            terreno = Terreno(terreno_data["x"], terreno_data["y"], terreno_data["width"], terreno_data["height"])
            self.terrenos.add(terreno)

        for plataforma_data in level_data.get("plataformas", []):
            plataforma = Plataforma(plataforma_data["x"], plataforma_data["y"], plataforma_data["width"], plataforma_data["height"])
            self.plataformas.add(plataforma)

        for plataforma_movil_data in level_data.get("plataformas_moviles", []):
            plataforma_movil = Plataforma_movil(plataforma_movil_data["x"], plataforma_movil_data["y"],
                                                plataforma_movil_data["width"], plataforma_movil_data["height"],
                                                plataforma_movil_data["speed"], plataforma_movil_data["distance"],
                                                plataforma_movil_data["direction"])
            self.plataforma_movil.add(plataforma_movil)

        for trampa_data in level_data.get("trampas", []):
            trampa = Trap(trampa_data["x"], trampa_data["y"], trampa_data["width"], trampa_data["height"])
            self.trap.add(trampa)

        for vida_data in level_data.get("vidas", []):
            vida = Vida(vida_data["x"], vida_data["y"], vida_data["width"], vida_data["height"])
            self.vidas.add(vida)

        for fruta_data in level_data.get("frutas", []):
            fruta = Frutas(fruta_data["x"], fruta_data["y"], fruta_data["width"], fruta_data["height"])
            self.frutas.add(fruta)
            
        for check_point_data in level_data.get("check_point", []):
            check_point = Check_point( check_point_data["x"],  check_point_data["y"],  check_point_data["width"],  check_point_data["height"])
            self.checkpoint.add(check_point)
        
        for trofeo_data in level_data.get("trofeo", []):
            trofeo = Trofeo( trofeo_data["x"],  trofeo_data["y"],  trofeo_data["width"],  trofeo_data["height"])
            self.trofeo.add(trofeo)

    def update(self,screen):
        screen.blit(self.fondo_img,screen.get_rect())
        self.plataforma_movil.update()
        self.terrenos.draw(screen)
        self.plataformas.draw(screen)
        self.plataforma_movil.draw(screen)
        self.trap.draw(screen)
        self.frutas.draw(screen)
        self.vidas.draw(screen)
        self.checkpoint.draw(screen)
        if len(self.frutas) <= 0:
            self.trofeo.draw(screen)
    def eliminar_elementos(self):
        self.terrenos.empty()
        self.plataformas.empty()
        self.plataforma_movil.empty()
        self.trap.empty()
        self.vidas.empty()
        self.frutas.empty()
        self.checkpoint.empty()
        self.trofeo.empty()