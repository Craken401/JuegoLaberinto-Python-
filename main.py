import threading
import time
import random

# ==========================
# ElementoMapa
# ==========================
class ElementoMapa:
    """
    Clase base para todos los elementos del mapa en el juego.
    Equivale a ElementoMapa en Smalltalk.
    """

    def es_habitacion(self):
        return False

    def es_puerta(self):
        return False

    def es_pared(self):
        return False

    def entrar(self, bicho=None):
        """
        En Smalltalk se manejaba 'entrar:' con un argumento.
        Aquí, lo unificamos.
        """
        raise NotImplementedError("Debe implementarse en subclases")

    def recorrer(self, funcion):
        """
        En Smalltalk, cada ElementoMapa tenía un método 'recorrer:'.
        Por defecto, un 'ElementoMapa' simple no recorre nada más;
        solo aplica la función a sí mismo.
        """
        funcion(self)


# ==========================
# Decoradores
# ==========================
class Decorador(ElementoMapa):
    """
    Equivale a la clase Decorator.
    Tiene un 'em' (elementoMapa decorado).
    """
    def __init__(self, em):
        super().__init__()
        self.em = em

    def entrar(self, bicho=None):
        self.em.entrar(bicho)


class Bomba(Decorador):
    """
    Equivale a Bomba, con una variable 'activa'.
    """
    def __init__(self, em):
        super().__init__(em)
        self.activa = False

    def entrar(self, bicho=None):
        if self.activa:
            # En Smalltalk hay un "Transcript show: <bicho> 'Te has chocado con una bomba'"
            print(f"{bicho} Te has chocado con una bomba")
            # Podríamos quitarle vidas, etc.
        else:
            self.em.entrar(bicho)


# ==========================
# Paredes
# ==========================
class Pared(ElementoMapa):
    """
    Equivale a la clase Pared en Smalltalk.
    """
    def es_pared(self):
        return True

    def entrar(self, bicho=None):
        # "Transcript show: <bicho> 'ha chocado con una pared'"
        print(f"{bicho} ha chocado con una pared")


class ParedBomba(Pared):
    """
    Equivale a ParedBomba en Smalltalk, con variable 'activa'.
    """
    def __init__(self):
        super().__init__()
        self.activa = False

    def entrar(self, bicho=None):
        if self.activa:
            print(f"{bicho} ha chocado con una ParedBomba")
            # Podríamos manejar explosión
        else:
            print(f"{bicho} ha chocado con una pared bomba (inactiva)")


# ==========================
# Puerta
# ==========================
class Puerta(ElementoMapa):
    """
    Equivale a la clase Puerta, con atributos:
    - abierta (bool)
    - lado1, lado2 (dos Habitaciones, o lo que sea)
    """
    def __init__(self, lado1, lado2):
        super().__init__()
        self.abierta = False
        self.lado1 = lado1
        self.lado2 = lado2

    def es_puerta(self):
        return True

    def abrir(self):
        self.abierta = True
        # Equivale a "Transcript show: 'Puerta X-Y ABIERTA'"
        print(f"Puerta {self.lado1.num}-{self.lado2.num} ABIERTA")

    def cerrar(self):
        self.abierta = False
        print(f"Puerta {self.lado1.num}-{self.lado2.num} CERRADA")

    def entrar(self, bicho=None):
        """
        Smalltalk: si está abierta, mira si bicho.posicion == lado1 => mover a lado2, etc.
        Si está cerrada => 'La puerta está cerrada'
        """
        if self.abierta:
            if bicho and bicho.posicion == self.lado1:
                self.lado2.entrar(bicho)
            else:
                self.lado1.entrar(bicho)
        else:
            print("La puerta está cerrada")

    def recorrer(self, funcion):
        """
        Para emular el 'recorrer:' en Smalltalk, aplicamos la función
        a la propia puerta.
        """
        funcion(self)


# ==========================
# Habitacion
# ==========================
class Habitacion(ElementoMapa):
    """
    Equivale a la clase Habitacion (subclase de Contenedor en Smalltalk).
    Aquí la simplificamos con referencias directas a 'norte', 'sur', etc.
    """
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
        """
        Equivale a 'Habitacion>>entrar: alguien':
          Transcript show: <bicho> ' está en Habitacion X'
          bicho posicion: self
        """
        print(f"{bicho} está en Hab{self.num}")
        if bicho:
            bicho.posicion = self

    def conectar(self, direccion, elemento):
        setattr(self, direccion, elemento)

    def recorrer(self, funcion):
        """
        Emulamos que la Habitacion aplique 'funcion' a sí misma
        y luego recorra sus 4 lados si existen.
        """
        funcion(self)
        for lado in (self.norte, self.sur, self.este, self.oeste):
            if lado is not None:
                lado.recorrer(funcion)


# ==========================
# Laberinto
# ==========================
class Laberinto(ElementoMapa):
    """
    Equivale a la clase Laberinto (subclase de Contenedor).
    """
    def __init__(self):
        super().__init__()
        self.habitaciones = []

    def agregar_habitacion(self, habitacion):
        self.habitaciones.append(habitacion)

    def obtener_habitacion(self, num):
        return next((h for h in self.habitaciones if h.num == num), None)

    def entrar(self, bicho=None):
        """
        En Smalltalk, 'entrar: alguien' ponía al bicho en la hab1.
        """
        hab1 = self.obtener_habitacion(1)
        if hab1 and bicho:
            hab1.entrar(bicho)

    def recorrer(self, funcion):
        """
        Recorremos todas las habitaciones y sus contenidos.
        """
        for hab in self.habitaciones:
            hab.recorrer(funcion)


# ==========================
# Modos (Strategy)
# ==========================
class Modo:
    """
    Equivale a la clase abstracta Modo.
    """
    def actua(self, bicho):
        """
        Template Method:
        - (opcional) self.dormir(bicho)
        - self.caminar(bicho)
        - self.atacar(bicho)
        """
        # Por ahora llamamos directamente a caminar y atacar
        self.caminar(bicho)
        self.atacar(bicho)

    def caminar(self, bicho):
        # El Smalltalk define 'caminar:unBicho' => elige orientacion, etc.
        raise NotImplementedError("Debe implementarse en subclases")

    def atacar(self, bicho):
        # En Smalltalk: 'no hace nada' por defecto
        pass

    def dormir(self, bicho):
        raise NotImplementedError("Debe implementarse en subclases")

    def es_agresivo(self):
        return False

    def es_perezoso(self):
        return False


class Agresivo(Modo):
    """
    Equivale a 'Agresivo' en Smalltalk.
    """
    def es_agresivo(self):
        return True

    def caminar(self, bicho):
        # El Smalltalk coge "or = bicho obtenerOrientacion" y camina
        orientacion = bicho.obtener_orientacion()
        if orientacion:
            orientacion.caminar(bicho)

    def dormir(self, bicho):
        print(f"{bicho} duerme (Agresivo) 1 segundo")
        time.sleep(1)


class Perezoso(Modo):
    """
    Equivale a 'Perezoso' en Smalltalk.
    """
    def es_perezoso(self):
        return True

    def caminar(self, bicho):
        # El Smalltalk coge "or = bicho obtenerOrientacion" y camina
        orientacion = bicho.obtener_orientacion()
        if orientacion:
            orientacion.caminar(bicho)

    def dormir(self, bicho):
        print(f"{bicho} duerme (Perezoso) 3 segundos")
        time.sleep(3)


# ==========================
# Bicho
# ==========================
class Bicho:
    """
    Equivale a la clase Bicho en Smalltalk.
    Atributos: vidas, poder, modo (Agresivo/Perezoso), posicion (Habitacion)
    """
    def __init__(self):
        self.vidas = 5
        self.poder = 1
        self.modo = None
        self.posicion = None

    def __str__(self):
        # Para que al hacer 'print(bicho)' salga algo amigable
        return f"Bicho(vidas={self.vidas})"

    def esta_vivo(self):
        return self.vidas > 0

    def actua(self):
        if self.modo:
            self.modo.actua(self)

    def ini_agresivo(self):
        self.modo = Agresivo()
        self.poder = 10

    def ini_perezoso(self):
        self.modo = Perezoso()
        self.poder = 1

    def es_agresivo(self):
        return self.modo is not None and self.modo.es_agresivo()

    def es_perezoso(self):
        return self.modo is not None and self.modo.es_perezoso()

    def obtener_orientacion(self):
        """
        Equivale a 'bicho obtenerOrientacion => bicho posicion obtenerOrientacion'
        En smalltalk: ^self posicion obtenerOrientacion
        """
        if self.posicion and hasattr(self.posicion, 'obtenerOrientacion'):
            # Devuelve una 'Orientacion' aleatoria de la lista
            return self.posicion.obtenerOrientacion()
        return None


# ==========================
# Orientaciones
# ==========================
class Orientacion:
    """
    Equivale a la clase abstracta Orientacion (Norte, Sur, Este, Oeste).
    """
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
# Creator y CreatorB
# ==========================
class Creator:
    """
    Equivale a la clase Creator en Smalltalk
    (fábrica de paredes, puertas, habitaciones, etc.).
    """
    def fabricar_habitacion(self, num):
        hab = Habitacion(num)
        hab.norte = self.fabricar_pared()
        hab.sur = self.fabricar_pared()
        hab.este = self.fabricar_pared()
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
        bicho = Bicho()
        bicho.ini_agresivo()
        return bicho

    def fabricar_bicho_perezoso(self):
        bicho = Bicho()
        bicho.ini_perezoso()
        return bicho

    def cambiar_a_modo_agresivo(self, bicho):
        bicho.ini_agresivo()


class CreatorB(Creator):
    """
    Equivale a CreatorB en Smalltalk, donde fabricar_pared() -> ParedBomba.
    """
    def fabricar_pared(self):
        return ParedBomba()


# ==========================
# Juego
# ==========================
class Juego:
    """
    Equivale a la clase Juego en Smalltalk
    Maneja la instancia de Laberinto y colecciones de Bichos.
    """
    def __init__(self):
        self.laberinto = Laberinto()
        self.bichos = []
        self.hilos = dict()  # Equivale a Dictionary new.

    def agregar_bicho(self, bicho):
        self.bichos.append(bicho)

    def eliminar_bicho(self, bicho):
        if bicho in self.bichos:
            self.bichos.remove(bicho)
        else:
            print("No existe ese bicho")

    def terminar_bicho(self, bicho):
        bicho.vidas = 0

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

    def abrir_puertas(self):
        """
        Equivale a 'abrirPuertas': recorre todo el laberinto y abre cada puerta.
        """
        def abrir_si_puerta(e):
            if e.es_puerta():
                e.abrir()
        self.laberinto.recorrer(abrir_si_puerta)

    def cerrar_puertas(self):
        """
        Equivale a 'cerrarPuertas': recorre todo el laberinto y cierra cada puerta.
        """
        def cerrar_si_puerta(e):
            if e.es_puerta():
                e.cerrar()
        self.laberinto.recorrer(cerrar_si_puerta)

    def lanzar_bicho(self, bicho):
        """
        Equivale a 'lanzarBicho:unBicho' => crea un thread que mientras el bicho viva,
        lo hace 'actua'.
        """
        def hilo_bicho():
            while bicho.esta_vivo():
                bicho.actua()
                # Podríamos hacer un pequeño sleep para no saturar
                time.sleep(0.2)
        t = threading.Thread(target=hilo_bicho)
        t.start()
        self.hilos[bicho] = t

    def lanzar_bichos(self):
        """
        Equivale a 'lanzarBichos': recorre self.bichos y lanza cada uno.
        """
        for b in self.bichos:
            self.lanzar_bicho(b)
