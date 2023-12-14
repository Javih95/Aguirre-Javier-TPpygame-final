def formatear_puntaje(puntaje: str) -> str:
    puntaje = str(puntaje).zfill(5)
    return puntaje

def formatear_nombre_jugador(nombre: str) -> str:
    nombre = nombre.strip().upper()
    if len(nombre) > 9:
        nombre = nombre[:9 - 3] + "..."
    return nombre
