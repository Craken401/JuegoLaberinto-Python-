import json
import time
import threading
import random

# =========================================
# ===============  ENTES  =================
# =========================================
class Ente:
    """
    Equivale a la clase 'Ente' en Smalltalk.
    Bicho y Personaje heredan de aquí.
    """
    def __init__(self):
        self.vidas = 5
        self.poder = 1
        self.posicion = None
        self.juego = None  # referencia al Juego

    def esta_vivo(self):
        return self.vidas > 0

    def es_atacado_por(self, atacante):
        """
        Smalltalk: esAtacadoPor:
        Resta vidas y, si llega a 0, llama a he_muerto().
        """
        print(f"{self} es atacado por {atacante}")
        self.vidas -= atacante.poder
        print(f"Vidas de {self}: {self.vidas}")
        if self.vidas <= 0:
            self.he_muerto()

    def he_muerto(self):
        """
        Subclase (Bicho o Personaje) debe implementar la lógica final
        (avisar al juego de que muere).
        """
        raise NotImplementedError("Subclase debe implementarlo")

    def __str__(self):
        return f"Ente(vidas={self.vidas})"


class Bicho(Ente):
    """
    Equivale a Bicho en Smalltalk. Tiene un 'modo' (Agresivo/Perezoso).
    """
    def __init__(self):
        super().__init__()
        self.modo = None  # Agresivo o Perezoso

    def he_muerto(self):
        # Smalltalk: juego terminarBicho:self
        if self.juego:
            self.juego.terminar_bicho(self)
        else:
            print("Bicho muere sin 'juego' asignado.")

    def actua(self):
        """
        Llama a modo.actua(self).
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
        Smalltalk: self juego buscarPersonaje:self
        """
        if self.juego:
            self.juego.buscar_personaje(self)

    def obtener_orientacion(self):
        """
        Equivale a 'posicion obtenerOrientacion' en Smalltalk.
        """
        if self.posicion and hasattr(self.posicion, 'obtener_orientacion'):
            return self.posicion.obtener_orientacion()
        return None

    def __str__(self):
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


class Personaje(Ente):
    """
    Equivale a la clase Personaje en Smalltalk.
    """
    def __init__(self, nombre):
        super().__init__()
        self.nombre = nombre

    def atacar(self):
        """
        Smalltalk: self juego buscarBichos:self
        """
        if self.juego:
            self.juego.buscar_bichos(self)

    def he_muerto(self):
        # Smalltalk: juego muerePersonaje
        if self.juego:
            self.juego.muere_personaje()
        else:
            print("Personaje muere sin 'juego' asignado.")

    def __str__(self):
        return f"Personaje({self.nombre}, vidas={self.vidas})"


# =========================================
# ===============   MODO   ================
# =========================================
class Modo:
    """
    Interfaz para Agresivo / Perezoso.
    En Smalltalk: la template: actua => dormir, caminar, atacar
    """
    def actua(self, bicho):
        self.dormir(bicho)
        self.caminar(bicho)
        self.atacar(bicho)

    def caminar(self, bicho):
        raise NotImplementedError("Subclase debe implementarlo")

    def atacar(self, bicho):
        bicho.atacar()

    def dormir(self, bicho):
        raise NotImplementedError("Subclase debe implementarlo")

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


# =========================================
# ===========  ELEMENTO MAPA  =============
# =========================================
class ElementoMapa:
    """
    Equivale a 'ElementoMapa' en Smalltalk (puede ser Pared, Puerta, etc.)
    """
    def es_habitacion(self):
        return False

    def es_puerta(self):
        return False

    def es_pared(self):
        return False

    def entrar(self, alguien):
        raise NotImplementedError("Subclase debe implementarlo")

    def recorrer(self, funcion):
        # Por defecto, solo se aplica la función a uno mismo.
        funcion(self)


# =========================================
# ===========  DECORADORES  ===============
# =========================================
class Decorador(ElementoMapa):
    def __init__(self, em):
        super().__init__()
        self.em = em

    def entrar(self, alguien):
        self.em.entrar(alguien)


class Bomba(Decorador):
    """
    Equivale a la clase Bomba en Smalltalk (un decorador).
    """
    def __init__(self, em):
        super().__init__(em)
        self.activa = False

    def entrar(self, alguien):
        if self.activa:
            print(f"{alguien} Te has chocado con una bomba (activa).")
            # Podríamos restar vidas, etc.
        else:
            self.em.entrar(alguien)

    def esBomba(self):
        return True

    def __str__(self):
        return f"Bomba(activa={self.activa})"


class Pared(ElementoMapa):
    def es_pared(self):
        return True

    def entrar(self, alguien):
        print(f"{alguien} ha chocado con una pared")


class ParedBomba(Pared):
    """
    Subclase de Pared que tiene 'activa'.
    """
    def __init__(self):
        super().__init__()
        self.activa = False

    def entrar(self, alguien):
        if self.activa:
            print(f"{alguien} ha chocado con una ParedBomba (activa)")
        else:
            print(f"{alguien} ha chocado con una ParedBomba (inactiva)")


class Puerta(ElementoMapa):
    """
    Equivale a Puerta en Smalltalk, con .abierta, .lado1, .lado2
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
        if hasattr(self.lado1, 'num') and hasattr(self.lado2, 'num'):
            print(f"Puerta {self.lado1.num}-{self.lado2.num} ABIERTA")
        else:
            print("Puerta ABIERTA (no num)")

    def cerrar(self):
        self.abierta = False
        if hasattr(self.lado1, 'num') and hasattr(self.lado2, 'num'):
            print(f"Puerta {self.lado1.num}-{self.lado2.num} CERRADA")
        else:
            print("Puerta CERRADA (no num)")

    def entrar(self, alguien):
        if self.abierta:
            if alguien and alguien.posicion == self.lado1:
                self.lado2.entrar(alguien)
            else:
                self.lado1.entrar(alguien)
        else:
            print("La puerta está cerrada")


# =========================================
# ===========   HABITACIONES  =============
# =========================================
class Habitacion(ElementoMapa):
    """
    Equivale a Habitacion en Smalltalk.
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

    def entrar(self, alguien):
        print(f"{alguien} está en Hab{self.num}")
        if alguien:
            alguien.posicion = self

    def conectar(self, direccion, elemento):
        # Por ejemplo: direccion="norte", elemento=Puerta u otra
        setattr(self, direccion, elemento)

    def recorrer(self, funcion):
        funcion(self)
        for lado in (self.norte, self.sur, self.este, self.oeste):
            if lado is not None:
                lado.recorrer(funcion)

    def __str__(self):
        return f"Hab{self.num}"


class Armario(Habitacion):
    """
    Equivale a 'Armario' en Smalltalk (subclase de Contenedor).
    """
    def __init__(self, num):
        super().__init__(num)

    def entrar(self, alguien):
        print(f"{alguien} se esconde en el armario Hab{self.num}")
        if alguien:
            alguien.posicion = self


class Laberinto(ElementoMapa):
    """
    Equivale a 'Laberinto' en Smalltalk (Contenedor de Habitaciones).
    """
    def __init__(self):
        super().__init__()
        self.habitaciones = []

    def agregar_habitacion(self, hab):
        self.habitaciones.append(hab)

    def obtener_habitacion(self, num):
        for h in self.habitaciones:
            if h.num == num:
                return h
        return None

    def entrar(self, alguien):
        # Equivalente a la lógica de: obtenerHabitacion(1).entrar(alguien)
        hab1 = self.obtener_habitacion(1)
        if hab1:
            hab1.entrar(alguien)

    def recorrer(self, funcion):
        for h in self.habitaciones:
            h.recorrer(funcion)

    def __str__(self):
        return "Laberinto"


# =========================================
# ============= ORIENTACIONES =============
# =========================================
class Orientacion:
    def caminar(self, bicho):
        raise NotImplementedError("Subclase debe implementarlo")

    def obtenerElementoOrEn(self, contenedor):
        raise NotImplementedError("Subclase debe implementarlo")

    def ponerElemento(self, elemento, contenedor):
        raise NotImplementedError("Subclase debe implementarlo")

    def recorrer(self, funcion, contenedor):
        raise NotImplementedError("Subclase debe implementarlo")


class Este(Orientacion):
    def caminar(self, bicho):
        if bicho.posicion and bicho.posicion.este:
            bicho.posicion.este.entrar(bicho)

    def obtenerElementoOrEn(self, contenedor):
        return contenedor.este

    def ponerElemento(self, elemento, contenedor):
        contenedor.este = elemento

    def recorrer(self, funcion, contenedor):
        if contenedor.este:
            contenedor.este.recorrer(funcion)


class Norte(Orientacion):
    def caminar(self, bicho):
        if bicho.posicion and bicho.posicion.norte:
            bicho.posicion.norte.entrar(bicho)

    def obtenerElementoOrEn(self, contenedor):
        return contenedor.norte

    def ponerElemento(self, elemento, contenedor):
        contenedor.norte = elemento

    def recorrer(self, funcion, contenedor):
        if contenedor.norte:
            contenedor.norte.recorrer(funcion)


class Oeste(Orientacion):
    def caminar(self, bicho):
        if bicho.posicion and bicho.posicion.oeste:
            bicho.posicion.oeste.entrar(bicho)

    def obtenerElementoOrEn(self, contenedor):
        return contenedor.oeste

    def ponerElemento(self, elemento, contenedor):
        contenedor.oeste = elemento

    def recorrer(self, funcion, contenedor):
        if contenedor.oeste:
            contenedor.oeste.recorrer(funcion)


class Sur(Orientacion):
    def caminar(self, bicho):
        if bicho.posicion and bicho.posicion.sur:
            bicho.posicion.sur.entrar(bicho)

    def obtenerElementoOrEn(self, contenedor):
        return contenedor.sur

    def ponerElemento(self, elemento, contenedor):
        contenedor.sur = elemento

    def recorrer(self, funcion, contenedor):
        if contenedor.sur:
            contenedor.sur.recorrer(funcion)


# =========================================
# ==============  FACTORY  ================
# =========================================
class Creator:
    """
    Equivale a la clase 'Creator' en Smalltalk (factory normal).
    """
    def fabricar_habitacion(self, num):
        hab = Habitacion(num)
        # Añadimos paredes por defecto:
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
        # En Smalltalk se hacía 'Bomba new', que es un decorador.
        # Por simplicidad: Bomba(None)
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
    """
    Equivale a CreatorB en Smalltalk (usa ParedBomba).
    """
    def fabricar_pared(self):
        return ParedBomba()


# =========================================
# ==============   JUEGO  =================
# =========================================
class Juego:
    """
    Equivale a la clase 'Juego' en Smalltalk.
    Contiene un Laberinto, lista de bichos, hilos, personaje, etc.
    """
    def __init__(self):
        self.laberinto = Laberinto()
        self.bichos = []
        self.hilos = {}
        self.person = None

    # -- Personaje --
    def agregar_personaje(self, nombre):
        p = Personaje(nombre)
        p.juego = self
        self.person = p
        self.laberinto.entrar(p)

    def muere_personaje(self):
        print("Fin del juego: ganan los bichos")
        self.terminar_bichos()

    def buscar_bichos(self, personaje):
        # Smalltalk: bichos do: ...
        for b in self.bichos:
            if b.posicion == personaje.posicion:
                b.es_atacado_por(personaje)

    def buscar_personaje(self, bicho):
        if self.person and bicho.posicion == self.person.posicion:
            self.person.es_atacado_por(bicho)

    def estan_todos_los_bichos_muertos(self):
        for b in self.bichos:
            if b.esta_vivo():
                return  # alguno sigue vivo
        # ninguno vivo:
        if self.person and self.person.esta_vivo():
            self.gana_personaje()

    def gana_personaje(self):
        print("Fin juego: gana el personaje")

    # -- Bichos --
    def agregar_bicho(self, bicho):
        self.bichos.append(bicho)
        bicho.juego = self

    def eliminar_bicho(self, bicho):
        try:
            self.bichos.remove(bicho)
        except ValueError:
            print("No existe ese bicho")

    def terminar_bicho(self, bicho):
        bicho.vidas = 0
        print(f"{bicho} muere")
        self.estan_todos_los_bichos_muertos()

    # -- Movimiento Personaje --
    def mover_personaje_hacia(self, orientacion):
        if self.person:
            self.person.caminar_hacia(orientacion)

    # -- Apertura / Cierre de puertas --
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

    # -- Hilos para bichos --
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
        for b in list(self.bichos):
            self.terminar_bicho(b)

    # -- Habitaciones (construcciones simples) --
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


# =========================================
# ==========  BUILDER (LaberintoBuilder)
# =========================================
class LaberintoBuilder:
    """
    Equivale a LaberintoBuilder en Smalltalk:
    - construye laberinto
    - construye juego
    - fabrica habitacion, armario, bomba, etc.
    """
    def __init__(self):
        self.juego = None
        self.laberinto = None

    def fabricar_juego(self):
        self.juego = Juego()
        # Asocia el laberinto al juego
        self.juego.laberinto = self.laberinto

    def fabricar_laberinto(self):
        self.laberinto = Laberinto()

    def fabricar_habitacion(self, num):
        h = Habitacion(num)
        # En Smalltalk se añadían orientaciones y paredes.
        # Aquí puedes emular el mismo comportamiento:
        h.norte = Pared()
        h.sur = Pared()
        h.este = Pared()
        h.oeste = Pared()
        # Se la agregamos al laberinto
        if self.laberinto:
            self.laberinto.agregar_habitacion(h)
        return h

    def fabricar_armario(self, num, contenedor):
        # En Smalltalk: Armario new, etc.
        arm = Armario(num)
        # Conectarle paredes/orientaciones si quieres
        arm.norte = Pared()
        arm.sur   = Pared()
        arm.este  = Pared()
        arm.oeste = Pared()
        # En Smalltalk se hacía contenedor.agregarHijo(arm).
        # Aquí, si contenedor es una Habitación,
        # podemos ponerlo en un costado o "hijos" (no formal en Python).
        # Por simplicidad, omitimos.
        # ...
        if isinstance(contenedor, Habitacion):
            # Podríamos "adjuntar" de algún modo. O nada.
            pass
        return arm

    def fabricar_bomba_en(self, contenedor):
        # Equivale a 'Bomba new' y contenedor agregarHijo.
        # En Python no tenemos 'agregarHijo' salvo que contenedor sea un Laberinto/Habitación
        # Se puede simular con un decorador, etc.
        # Simplificamos: no implementamos 'hijos' en habitacion.
        bomb = Bomba(None)
        # No hay un "agregarHijo" en Habitacion por defecto. 
        # Lo omitimos o definimos la lógica que quieras.
        # ...
        pass

    def fabricar_bicho_agresivo(self):
        b = Bicho()
        b.ini_agresivo()
        return b

    def fabricar_bicho_perezoso(self):
        b = Bicho()
        b.ini_perezoso()
        return b

    def fabricar_bicho_modo(self, modo_str, num_hab):
        """
        Equivale a 'fabricarBichoModo:posicion:' en Smalltalk.
        """
        # Depende de si modo_str = "Agresivo" o "Perezoso"
        if modo_str.lower() == "agresivo":
            b = self.fabricar_bicho_agresivo()
        else:
            b = self.fabricar_bicho_perezoso()

        hab = None
        if self.laberinto:
            hab = self.laberinto.obtener_habitacion(num_hab)
        if hab:
            hab.entrar(b)
        if self.juego:
            self.juego.agregar_bicho(b)

    def fabricar_pared(self):
        return Pared()

    def fabricar_puerta_l1(self, num1, or1, num2, or2):
        """
        En Smalltalk: fabricarPuertaL1:or1:L2:or2:
        num1 -> Habitacion 1
        or1  -> 'Sur', 'Norte', etc.
        num2 -> Habitacion 2
        or2  -> 'Sur', 'Norte', etc.
        """
        if not self.laberinto:
            return
        h1 = self.laberinto.obtener_habitacion(num1)
        h2 = self.laberinto.obtener_habitacion(num2)

        if not h1 or not h2:
            return
        # Convert or1 -> clase orientacion?
        # En Smalltalk se usaba perform:('fabricar'+or1)
        # Aquí lo simplificamos: creamos la puerta y la asignamos.
        pt = Puerta(h1, h2)

        # Asignamos en la habitacion h1/h2
        if or1.lower() == "norte":
            h1.norte = pt
        elif or1.lower() == "sur":
            h1.sur = pt
        elif or1.lower() == "este":
            h1.este = pt
        elif or1.lower() == "oeste":
            h1.oeste = pt

        if or2.lower() == "norte":
            h2.norte = pt
        elif or2.lower() == "sur":
            h2.sur = pt
        elif or2.lower() == "este":
            h2.este = pt
        elif or2.lower() == "oeste":
            h2.oeste = pt

    def obtener_juego(self):
        return self.juego


# =========================================
# =============   DIRECTOR   ==============
# =========================================
class Director:
    """
    Equivale a Director en Smalltalk.
    - leer JSON
    - crear builder
    - fabricar laberinto, juego, bichos
    """
    def __init__(self):
        self.builder = None
        self.dict_data = {}

    def leer_archivo(self, archivo_json):
        with open(archivo_json, 'r', encoding='utf-8') as f:
            self.dict_data = json.load(f)

    def ini_builder(self):
        self.builder = LaberintoBuilder()

    def fabricar_laberinto(self):
        self.builder.fabricar_laberinto()
        # Recorrer "laberinto" del JSON
        laberinto_list = self.dict_data.get("laberinto", [])
        for elem in laberinto_list:
            self.fabricar_laberinto_recursivo(elem, "root")

        # Recorrer "puertas"
        puertas_list = self.dict_data.get("puertas", [])
        for p in puertas_list:
            # Ej: [1, "Sur", 2, "Norte"]
            num1, or1, num2, or2 = p
            self.builder.fabricar_puerta_l1(num1, or1, num2, or2)

    def fabricar_juego(self):
        self.builder.fabricar_juego()

    def fabricar_bichos(self):
        bichos_list = self.dict_data.get("bichos", [])
        for b in bichos_list:
            modo = b.get("modo", "Perezoso")
            pos = b.get("posicion", 1)
            self.builder.fabricar_bicho_modo(modo, pos)

    def fabricar_laberinto_recursivo(self, unDic, padre):
        """
        En Smalltalk: si 'tipo'=='habitacion' -> fabricarHabitacion
                      si 'tipo'=='armario' -> fabricarArmario
                      si 'tipo'=='bomba' -> ...
        """
        tipo = unDic.get("tipo", "")
        con = None

        if tipo == "habitacion":
            con = self.builder.fabricar_habitacion(unDic["num"])
        elif tipo == "armario":
            # padre no se usa mucho en Python, pero lo dejamos:
            con = self.builder.fabricar_armario(unDic["num"], padre)
        elif tipo == "bomba":
            # añade una bomba a 'padre'
            self.builder.fabricar_bomba_en(padre)

        # hijos recursivos
        hijos = unDic.get("hijos", [])
        for h in hijos:
            self.fabricar_laberinto_recursivo(h, con)

    def procesar(self, archivo_json):
        """
        Smalltalk: leerArchivo:; iniBuilder; fabricarLaberinto; fabricarJuego; fabricarBichos
        """
        self.leer_archivo(archivo_json)
        self.ini_builder()
        self.fabricar_laberinto()
        self.fabricar_juego()
        self.fabricar_bichos()

    def obtener_juego(self):
        return self.builder.obtener_juego()
