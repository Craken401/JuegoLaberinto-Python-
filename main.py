import threading
import time
import random

# ==========================
# Ente (base de Personaje y Bicho)
# ==========================
class Ente:
    """
    En Smalltalk, tanto 'Bicho' como 'Personaje' heredan de un 'Ente' con:
     - vidas
     - poder
     - posicion
     - juego (referencia al 'Juego' para avisar de muertes, etc.)
    """

    def __init__(self):
        self.vidas = 5
        self.poder = 1
        self.posicion = None
        self.juego = None  # Para que sepa en qué juego está

    def esta_vivo(self):
        return self.vidas > 0

    def es_atacado_por(self, atacante):
        """
        Equivale a 'self esAtacadoPor: unBicho/unPersonaje' en Smalltalk.
        Resta vidas y, si llega a 0, llama a he_muerto().
        """
        print(f"{self} es atacado por {atacante}")
        self.vidas -= atacante.poder
        print(f"Vidas de {self}: {self.vidas}")
        if self.vidas <= 0:
            self.he_muerto()

    def he_muerto(self):
        """
        En Smalltalk, Bicho hace: self juego terminarBicho:self
        Personaje hace: self juego muerePersonaje
        Aquí lo dejamos abstracto; subclases lo implementan.
        """
        raise NotImplementedError("Subclase debe implementarlo")

    def __str__(self):
        return f"Ente(vidas={self.vidas})"


# ==========================
# Bicho (subclase de Ente)
# ==========================
class Bicho(Ente):
    """
    Equivale a la clase Bicho en Smalltalk, pero ahora hereda de Ente.
    Tiene un 'modo' (Agresivo/Perezoso) y un método 'atacar' (busca al Personaje).
    """

    def __init__(self):
        super().__init__()
        self.modo = None  # Modo (Agresivo/Perezoso)

    def he_muerto(self):
        """
        Equivale a Bicho>>heMuerto => self juego terminarBicho:self
        """
        if self.juego:
            self.juego.terminar_bicho(self)
        else:
            print("Bicho muere, pero no hay juego definido.")

    def actua(self):
        """
        El bucle principal del bicho en Smalltalk: modo.actua(self).
        """
        if self.modo:
            self.modo.actua(self)

    def ini_agresivo(self):
        self.modo = Agresivo()
        self.poder = 10

    def ini_perezoso(self):
        self.modo = Perezoso()
        self.poder = 1

    def atacar(self):
        """
        En Smalltalk: self juego buscarPersonaje:self
        """
        if self.juego:
            self.juego.buscar_personaje(self)

    def obtener_orientacion(self):
        """
        Equivale a 'bicho posicion obtenerOrientacion' en Smalltalk.
        """
        if self.posicion and hasattr(self.posicion, 'obtenerOrientacion'):
            return self.posicion.obtenerOrientacion()
        return None

    def __str__(self):
        # Mostrar "Bicho-Agresivo" o "Bicho-Perezoso" según el modo:
        if self.modo:
            if self.modo.es_agresivo():
                modo_str = "Agresivo"
            elif self.modo.es_perezoso():
                modo_str = "Perezoso"
            else:
                modo_str = "Desconocido"
        else:
            modo_str = "SinModo"
        return f"Bicho({modo_str}, vidas={self.vidas})"


# ==========================
# Personaje (subclase de Ente)
# ==========================
class Personaje(Ente):
    """
    Equivale a la clase Personaje (usuario/jugador) en Smalltalk.
    """

    def __init__(self, nombre):
        super().__init__()
        self.nombre = nombre

    def atacar(self):
        """
        En Smalltalk: self juego buscarBichos:self
        (Ataca a todos los bichos en su misma habitación.)
        """
        if self.juego:
            self.juego.buscar_bichos(self)

    def he_muerto(self):
        """
        Equivale a Personaje>>heMuerto => self juego muerePersonaje
        """
        if self.juego:
            self.juego.muere_personaje()
        else:
            print("Personaje muere, pero no hay juego definido.")

    def __str__(self):
        return f"Personaje({self.nombre}, vidas={self.vidas})"


# ==========================
# Modo (Agresivo / Perezoso)
# ==========================
class Modo:
    """
    Clase abstracta. 'actua:' en Smalltalk se hace con:
      - dormir(bicho)
      - caminar(bicho)
      - atacar(bicho)
    """

    def actua(self, bicho):
        # Template Method
        self.dormir(bicho)
        self.caminar(bicho)
        self.atacar(bicho)

    def caminar(self, bicho):
        raise NotImplementedError("Debe implementarse en subclases")

    def atacar(self, bicho):
        # Por defecto, no hace nada
        bicho.atacar()

    def dormir(self, bicho):
        raise NotImplementedError("Debe implementarse en subclases")

    def es_agresivo(self):
        return False

    def es_perezoso(self):
        return False


class Agresivo(Modo):
    def es_agresivo(self):
        return True

    def caminar(self, bicho):
        orientacion = bicho.obtener_orientacion()
        if orientacion:
            orientacion.caminar(bicho)

    def dormir(self, bicho):
        print(f"{bicho} duerme (Agresivo) 1 segundo")
        time.sleep(1)


class Perezoso(Modo):
    def es_perezoso(self):
        return True

    def caminar(self, bicho):
        orientacion = bicho.obtener_orientacion()
        if orientacion:
            orientacion.caminar(bicho)

    def dormir(self, bicho):
        print(f"{bicho} duerme (Perezoso) 3 segundos")
        time.sleep(3)


# ==========================
# ElementoMapa base
# ==========================
class ElementoMapa:
    """
    Clase base (Smalltalk: ElementoMapa).
    """

    def es_habitacion(self):
        return False

    def es_puerta(self):
        return False

    def es_pared(self):
        return False

    def entrar(self, alguien=None):
        raise NotImplementedError("Debe implementarse en subclases")

    def recorrer(self, funcion):
        funcion(self)


# ==========================
# Decorador / Bomba
# ==========================
class Decorador(ElementoMapa):
    def __init__(self, em):
        super().__init__()
        self.em = em

    def entrar(self, bicho=None):
        self.em.entrar(bicho)


class Bomba(Decorador):
    def __init__(self, em):
        super().__init__(em)
        self.activa = False

    def entrar(self, bicho=None):
        if self.activa:
            print(f"{bicho} Te has chocado con una bomba")
            # Podríamos bajar vidas, etc.
        else:
            self.em.entrar(bicho)


# ==========================
# Pared y ParedBomba
# ==========================
class Pared(ElementoMapa):
    def es_pared(self):
        return True

    def entrar(self, bicho=None):
        print(f"{bicho} ha chocado con una pared")


class ParedBomba(Pared):
    def __init__(self):
        super().__init__()
        self.activa = False

    def entrar(self, bicho=None):
        if self.activa:
            print(f"{bicho} ha chocado con una ParedBomba (activa)")
        else:
            print(f"{bicho} ha chocado con una ParedBomba (inactiva)")


# ==========================
# Puerta
# ==========================
class Puerta(ElementoMapa):
    def __init__(self, lado1, lado2):
        super().__init__()
        self.abierta = False
        self.lado1 = lado1
        self.lado2 = lado2

    def es_puerta(self):
        return True

    def abrir(self):
        self.abierta = True
        print(f"Puerta {self.lado1.num}-{self.lado2.num} ABIERTA")

    def cerrar(self):
        self.abierta = False
        print(f"Puerta {self.lado1.num}-{self.lado2.num} CERRADA")

    def entrar(self, bicho=None):
        if self.abierta:
            if bicho and bicho.posicion == self.lado1:
                self.lado2.entrar(bicho)
            else:
                self.lado1.entrar(bicho)
        else:
            print("La puerta está cerrada")

    def recorrer(self, funcion):
        funcion(self)


# ==========================
# Habitacion
# ==========================
class Habitacion(ElementoMapa):
    def __init__(self, num):
        super().__init__()
        self.num = num
        self.norte = None
        self.sur = None
        self.este = None
        self.oeste = None

    def es_habitacion(self):
        return True

    def entrar(self, bicho=None):
        print(f"{bicho} está en Hab{self.num}")
        if bicho:
            bicho.posicion = self

    def conectar(self, direccion, elemento):
        setattr(self, direccion, elemento)

    def recorrer(self, funcion):
        funcion(self)
        for lado in (self.norte, self.sur, self.este, self.oeste):
            if lado is not None:
                lado.recorrer(funcion)


# ==========================
# Laberinto
# ==========================
class Laberinto(ElementoMapa):
    def __init__(self):
        super().__init__()
        self.habitaciones = []

    def agregar_habitacion(self, habitacion):
        self.habitaciones.append(habitacion)

    def obtener_habitacion(self, num):
        return next((h for h in self.habitaciones if h.num == num), None)

    def entrar(self, bicho=None):
        hab1 = self.obtener_habitacion(1)
        if hab1 and bicho:
            hab1.entrar(bicho)

    def recorrer(self, funcion):
        for hab in self.habitaciones:
            hab.recorrer(funcion)


# ==========================
# Orientaciones (Norte, Sur, Este, Oeste)
# ==========================
class Orientacion:
    def caminar(self, bicho):
        raise NotImplementedError("Subclase debe implementarlo")

    def obtenerElementoOrEn(self, unContenedor):
        raise NotImplementedError("Subclase debe implementarlo")

    def ponerElemento(self, unEM, unContenedor):
        raise NotImplementedError("Subclase debe implementarlo")

    def recorrer(self, funcion, contenedor=None):
        raise NotImplementedError("Subclase debe implementarlo")


class Este(Orientacion):
    def caminar(self, bicho):
        if bicho.posicion and bicho.posicion.este:
            bicho.posicion.este.entrar(bicho)

    def obtenerElementoOrEn(self, unContenedor):
        return unContenedor.este

    def ponerElemento(self, unEM, unContenedor):
        unContenedor.este = unEM

    def recorrer(self, funcion, contenedor=None):
        if contenedor and contenedor.este:
            contenedor.este.recorrer(funcion)


class Norte(Orientacion):
    def caminar(self, bicho):
        if bicho.posicion and bicho.posicion.norte:
            bicho.posicion.norte.entrar(bicho)

    def obtenerElementoOrEn(self, unContenedor):
        return unContenedor.norte

    def ponerElemento(self, unEM, unContenedor):
        unContenedor.norte = unEM

    def recorrer(self, funcion, contenedor=None):
        if contenedor and contenedor.norte:
            contenedor.norte.recorrer(funcion)


class Oeste(Orientacion):
    def caminar(self, bicho):
        if bicho.posicion and bicho.posicion.oeste:
            bicho.posicion.oeste.entrar(bicho)

    def obtenerElementoOrEn(self, unContenedor):
        return unContenedor.oeste

    def ponerElemento(self, unEM, unContenedor):
        unContenedor.oeste = unEM

    def recorrer(self, funcion, contenedor=None):
        if contenedor and contenedor.oeste:
            contenedor.oeste.recorrer(funcion)


class Sur(Orientacion):
    def caminar(self, bicho):
        if bicho.posicion and bicho.posicion.sur:
            bicho.posicion.sur.entrar(bicho)

    def obtenerElementoOrEn(self, unContenedor):
        return unContenedor.sur

    def ponerElemento(self, unEM, unContenedor):
        unContenedor.sur = unEM

    def recorrer(self, funcion, contenedor=None):
        if contenedor and contenedor.sur:
            contenedor.sur.recorrer(funcion)


# ==========================
# Creator / CreatorB
# ==========================
class Creator:
    def fabricar_habitacion(self, num):
        hab = Habitacion(num)
        # En Smalltalk se agregan orientaciones. Simplificamos conectando paredes:
        hab.norte = self.fabricar_pared()
        hab.sur   = self.fabricar_pared()
        hab.este  = self.fabricar_pared()
        hab.oeste = self.fabricar_pared()
        return hab

    def fabricar_juego(self):
        return Juego()

    def fabricar_laberinto(self):
        return Laberinto()

    def fabricar_pared(self):
        return Pared()

    def fabricar_puerta(self, lado1, lado2):
        return Puerta(lado1, lado2)

    def fabricar_bomba(self):
        return Bomba(None)

    def fabricar_bicho_agresivo(self):
        b = Bicho()
        b.ini_agresivo()
        return b

    def fabricar_bicho_perezoso(self):
        b = Bicho()
        b.ini_perezoso()
        return b

    def cambiar_a_modo_agresivo(self, bicho):
        bicho.ini_agresivo()


class CreatorB(Creator):
    def fabricar_pared(self):
        return ParedBomba()


# ==========================
# Juego
# ==========================
class Juego:
    def __init__(self):
        self.laberinto = Laberinto()
        self.bichos = []
        self.hilos = {}
        self.person = None  # En Smalltalk: 'person'

    # -------- Personaje --------
    def agregar_personaje(self, nombre):
        p = Personaje(nombre)
        p.juego = self
        self.person = p
        # En Smalltalk: self laberinto entrar: self person
        self.laberinto.entrar(self.person)

    def muere_personaje(self):
        print("Fin del juego: ganan los bichos")
        self.terminar_bichos()

    def buscar_bichos(self, unPersonaje):
        """
        En Smalltalk: 'self bichos do: [:b | if b.posicion = unPersonaje.posicion then b esAtacadoPor:unPersonaje]'
        """
        for b in self.bichos:
            if b.posicion == unPersonaje.posicion:
                b.es_atacado_por(unPersonaje)

    def buscar_personaje(self, unBicho):
        """
        En Smalltalk: 'posBicho=posPerson => self person esAtacadoPor: unBicho'
        """
        if self.person and unBicho.posicion == self.person.posicion:
            self.person.es_atacado_por(unBicho)

    def estan_todos_los_bichos_muertos(self):
        """
        En Smalltalk: detect un bicho vivo. Si no hay ninguno y el Personaje vive, => ganaPersonaje.
        """
        for b in self.bichos:
            if b.esta_vivo():
                return  # hay al menos un bicho vivo, no pasa nada
        # Si llegamos aquí, ninguno está vivo:
        if self.person and self.person.esta_vivo():
            self.gana_personaje()

    def gana_personaje(self):
        print("Fin juego: gana el personaje")

    # -------- Bichos --------
    def agregar_bicho(self, bicho):
        self.bichos.append(bicho)
        bicho.juego = self

    def eliminar_bicho(self, bicho):
        if bicho in self.bichos:
            self.bichos.remove(bicho)
        else:
            print("No existe ese bicho")

    def terminar_bicho(self, bicho):
        bicho.vidas = 0
        print(f"{bicho} muere")
        # Chequea si están todos muertos:
        self.estan_todos_los_bichos_muertos()

    # -------- Movimientos Personaje --------
    def mover_personaje_hacia(self, orientacion):
        if self.person:
            self.person.caminar_hacia(orientacion)

    # -------- Laberintos Predefinidos --------
    def obtener_habitacion(self, num):
        return self.laberinto.obtener_habitacion(num)

    def crear_laberinto_2_habitaciones(self):
        hab1 = Habitacion(1)
        hab2 = Habitacion(2)

        hab1.este = Pared()
        hab1.oeste = Pared()
        hab1.norte = Pared()

        hab2.sur = Pared()
        hab2.este = Pared()
        hab2.oeste = Pared()

        puerta = Puerta(hab1, hab2)
        hab1.sur = puerta
        hab2.norte = puerta

        self.laberinto = Laberinto()
        self.laberinto.agregar_habitacion(hab1)
        self.laberinto.agregar_habitacion(hab2)

        return self.laberinto

    def crear_laberinto_2_habitaciones_fm(self, creator):
        hab1 = creator.fabricar_habitacion(1)
        hab2 = creator.fabricar_habitacion(2)
        puerta = creator.fabricar_puerta(hab1, hab2)
        hab1.sur = puerta
        hab2.norte = puerta
        self.laberinto = creator.fabricar_laberinto()
        self.laberinto.agregar_habitacion(hab1)
        self.laberinto.agregar_habitacion(hab2)
        return self.laberinto

    def crear_laberinto_2_habitaciones_fmd(self, creator):
        hab1 = creator.fabricar_habitacion(1)
        hab2 = creator.fabricar_habitacion(2)

        bomba1 = creator.fabricar_bomba()
        bomba1.em = creator.fabricar_pared()
        hab1.este = bomba1

        bomba2 = creator.fabricar_bomba()
        bomba2.em = creator.fabricar_pared()
        hab2.este = bomba2

        puerta = creator.fabricar_puerta(hab1, hab2)
        hab1.sur = puerta
        hab2.norte = puerta

        self.laberinto = creator.fabricar_laberinto()
        self.laberinto.agregar_habitacion(hab1)
        self.laberinto.agregar_habitacion(hab2)
        return self.laberinto

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
        bicho_rojo2.posicion = hab2

        bicho_verde1 = Bicho()
        bicho_verde1.ini_perezoso()
        bicho_verde1.posicion = hab3

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

    # -------- Abrir / Cerrar Puertas --------
    def abrir_puertas(self):
        def abrir_si_puerta(e):
            if e.es_puerta():
                e.abrir()
        self.laberinto.recorrer(abrir_si_puerta)

    def cerrar_puertas(self):
        def cerrar_si_puerta(e):
            if e.es_puerta():
                e.cerrar()
        self.laberinto.recorrer(cerrar_si_puerta)

    # -------- Hilos (lanzarBicho / terminarBichos) --------
    def lanzar_bicho(self, bicho):
        def hilo_bicho():
            while bicho.esta_vivo():
                bicho.actua()
                time.sleep(0.2)
        t = threading.Thread(target=hilo_bicho)
        t.start()
        self.hilos[bicho] = t

    def lanzar_bichos(self):
        for b in self.bichos:
            self.lanzar_bicho(b)

    def terminar_bichos(self):
        """
        Equivale a 'terminarBichos': setea vidas=0 a todos y así paran sus hilos.
        """
        for b in list(self.bichos):
            self.terminar_bicho(b)
        # Podríamos join() los threads si quisiéramos.
