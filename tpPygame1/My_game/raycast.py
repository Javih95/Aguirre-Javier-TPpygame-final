import pygame
import random
class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction  # Normaliza la dirección del rayo

    def advance(self, distance):
        # Avanza el rayo en la dirección especificada
        random_distance = random.uniform(0, distance)
        self.origin += self.direction * random_distance
    def raycast(ray, objects):
        for obj in objects:
            if obj.rect.collidepoint(ray.origin):
                return True
        return False
