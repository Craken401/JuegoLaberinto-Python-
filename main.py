class ElementoMapa:
    def entrar(self):
        raise NotImplementedError("Debe ser implementado por las subclases")

class Habitacion(ElementoMapa):
    def __init__(self, num):
        self.num = num
        self.norte = None
        self.sur = None
        self.este = None
        self.oeste = None

class Laberinto(ElementoMapa):
    def __init__(self):
        self.habitaciones = []

    def agregar_habitacion(self, habitacion):
        self.habitaciones.append(habitacion)

class Pared(ElementoMapa):
    pass

class Puerta(ElementoMapa):
    def __init__(self, lado1, lado2):
        self.abierta = False
        self.lado1 = lado1
        self.lado2 = lado2
    
    def abrir(self):
        self.abierta = True
    
    def cerrar(self):
        self.abierta = False

class Juego:
    def __init__(self):
        self.laberinto = Laberinto()

# Implementación del Factory Method
class Creator:
    def fabricar_habitacion(self, num):
        hab = Habitacion(num)
        hab.este = self.fabricar_pared()
        hab.oeste = self.fabricar_pared()
        hab.norte = self.fabricar_pared()
        hab.sur = self.fabricar_pared()
        return hab

    def fabricar_juego(self):
        return Juego()
    
    def fabricar_laberinto(self):
        return Laberinto()
    
    def fabricar_pared(self):
        return Pared()
    
    def fabricar_puerta(self, lado1, lado2):
        return Puerta(lado1, lado2)
