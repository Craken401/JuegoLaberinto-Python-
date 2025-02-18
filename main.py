class ElementoMapa:
    def entrar(self):
        raise NotImplementedError("Debe ser implementado por las subclases")

class Decorador(ElementoMapa):
    def __init__(self, em):
        self.em = em
    
    def entrar(self):
        self.em.entrar()

class Bomba(Decorador):
    def __init__(self, em):
        super().__init__(em)
        self.activa = False
    
    def entrar(self):
        if self.activa:
            print("Te has chocado con una bomba")
        else:
            self.em.entrar()

class Habitacion(ElementoMapa):
    def __init__(self, num):
        self.num = num
        self.norte = None
        self.sur = None
        self.este = None
        self.oeste = None
    
    def conectar(self, direccion, elemento):
        setattr(self, direccion, elemento)

class Laberinto(ElementoMapa):
    def __init__(self):
        self.habitaciones = []
    
    def agregar_habitacion(self, habitacion):
        self.habitaciones.append(habitacion)
    
    def obtener_habitacion(self, num):
        return next((hab for hab in self.habitaciones if hab.num == num), None)

class Pared(ElementoMapa):
    def entrar(self):
        print("Te has chocado con una pared")

class ParedBomba(Pared):
    def __init__(self):
        self.activa = False
    
    def entrar(self):
        print("Te has chocado con una pared bomba")

class Puerta(ElementoMapa):
    def __init__(self, lado1, lado2):
        self.abierta = False
        self.lado1 = lado1
        self.lado2 = lado2
    
    def abrir(self):
        self.abierta = True
    
    def cerrar(self):
        self.abierta = False
    
    def entrar(self):
        if self.abierta:
            print("La puerta está abierta")
        else:
            print("La puerta está cerrada")

class Modo:
    def actua(self, bicho):
        self.camina(bicho)
    
    def camina(self, bicho):
        raise NotImplementedError("Debe implementarse en subclases")
    
    def es_agresivo(self):
        return False
    
    def es_perezoso(self):
        return False

class Agresivo(Modo):
    def es_agresivo(self):
        return True

class Perezoso(Modo):
    def es_perezoso(self):
        return True

class Bicho:
    def __init__(self):
        self.vidas = 5
        self.poder = 1
        self.modo = None
        self.posicion = None
    
    def actua(self):
        self.modo.actua(self)
    
    def ini_agresivo(self):
        self.modo = Agresivo()
        self.poder = 10
    
    def ini_perezoso(self):
        self.modo = Perezoso()
        self.poder = 1

class Juego:
    def __init__(self):
        self.laberinto = Laberinto()
        self.bichos = []
    
    def agregar_bicho(self, bicho):
        self.bichos.append(bicho)
    
    def eliminar_bicho(self, bicho):
        if bicho in self.bichos:
            self.bichos.remove(bicho)
        else:
            print("No existe ese bicho")
    
    def crear_laberinto_4_habitaciones(self):
        hab1 = Habitacion(1)
        hab2 = Habitacion(2)
        hab3 = Habitacion(3)
        hab4 = Habitacion(4)
        
        puerta1 = Puerta(hab1, hab2)
        puerta2 = Puerta(hab3, hab4)
        puerta3 = Puerta(hab1, hab3)
        puerta4 = Puerta(hab2, hab4)
        
        hab1.conectar("sur", puerta3)
        hab2.conectar("sur", puerta4)
        hab3.conectar("norte", puerta3)
        hab4.conectar("norte", puerta4)
        hab1.conectar("este", puerta1)
        hab2.conectar("oeste", puerta1)
        hab3.conectar("este", puerta2)
        hab4.conectar("oeste", puerta2)
        
        bicho_rojo1 = Bicho()
        bicho_rojo1.ini_agresivo()
        bicho_rojo1.posicion = hab1
        
        bicho_rojo2 = Bicho()
        bicho_rojo2.ini_agresivo()
        bicho_rojo2.posicion = hab3
        
        bicho_verde1 = Bicho()
        bicho_verde1.ini_perezoso()
        bicho_verde1.posicion = hab2
        
        bicho_verde2 = Bicho()
        bicho_verde2.ini_perezoso()
        bicho_verde2.posicion = hab4
        
        self.laberinto.agregar_habitacion(hab1)
        self.laberinto.agregar_habitacion(hab2)
        self.laberinto.agregar_habitacion(hab3)
        self.laberinto.agregar_habitacion(hab4)
        
        self.agregar_bicho(bicho_rojo1)
        self.agregar_bicho(bicho_rojo2)
        self.agregar_bicho(bicho_verde1)
        self.agregar_bicho(bicho_verde2)

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

class CreatorB(Creator):
    def fabricar_pared(self):
        return ParedBomba()
