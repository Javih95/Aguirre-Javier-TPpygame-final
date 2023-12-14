import json
class Manejo_de_datos:
    def __init__(self,archivo):
        self.lista_jugadores = []
        self.cargar_datos(archivo)
    def cargar_datos(self,archivo):
        try:
            with open(archivo) as file:
                datos = json.load(file)
                for jugador_datos in datos:
                    self.lista_jugadores.append(jugador_datos)
        except FileNotFoundError:
            print("error el archivo no se encuentra")
        except PermissionError:
            print("No tiene permiso de acceder  al archivo")
        except:
            print("Error inesperado")
    def guardar_datos(self,nombre,puntos,nombre_player):
        self.puntos = puntos
        self.nombre_player = nombre_player
        self.nombre= nombre
        self.nombre_archivo = ".json"
        datos_a_guardar = (self.nombre_player,self.puntos)
        self.lista_jugadores.append(datos_a_guardar)
        try:
            with open((self.nombre)+(self.nombre_archivo), "w+") as archivo:
                json.dump(self.lista_jugadores, archivo)
        except:
            print("error")