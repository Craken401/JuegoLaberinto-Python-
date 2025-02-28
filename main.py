class ElementoMapa:
    # =========================
    # Métodos de consulta (equivalentes a esHabitacion, esPuerta, esPared, etc.)
    # =========================
    def es_habitacion(self):
        return False
    
    def es_puerta(self):
        return False
    
    def es_pared(self):
        return False

    # =========================
    # Métodos de "entrar"
    # =========================
    def entrar(self):
        """
        Comportamiento al "entrar" en este elemento del mapa.
        Smalltalk usaba 'entrar' y 'entrar:'.
        En Python, por simplicidad, dejamos un solo 'entrar' que recibe o no
        un posible 'actor' si hiciera falta.
        """
        raise NotImplementedError("Debe ser implementado por las subclases")


class Decorador(ElementoMapa):
    """
    Equivale a la clase Decorator en Smalltalk,
    que tiene un 'em' (elementoMapa decorado).
    """
    def __init__(self, em):
        self.em = em
    
    def entrar(self):
        self.em.entrar()


class Bomba(Decorador):
    """
    Equivale a Bomba, que es un Decorator con una variable 'activa'.
    """
    def __init__(self, em):
        super().__init__(em)
        self.activa = False
    
    def entrar(self):
        if self.activa:
            print("Te has chocado con una bomba")
        else:
            self.em.entrar()


class Pared(ElementoMapa):
    """
    Equivale a la clase Pared normal en Smalltalk.
    """
    def es_pared(self):
        return True

    def entrar(self):
        print("Te has chocado con una pared")


class ParedBomba(Pared):
    """
    Equivale a ParedBomba, con una variable 'activa'.
    """
    def __init__(self):
        self.activa = False
    
    def entrar(self):
        print("Te has chocado con una pared bomba")


class Puerta(ElementoMapa):
    """
    Equivale a la clase Puerta, con atributos abierta, lado1, lado2.
    """
    def __init__(self, lado1, lado2):
        self.abierta = False
        self.lado1 = lado1
        self.lado2 = lado2
    
    def es_puerta(self):
        return True

    def abrir(self):
        self.abierta = True
    
    def cerrar(self):
        self.abierta = False
    
    def entrar(self):
        if self.abierta:
            print("La puerta está abierta")
        else:
            print("La puerta está cerrada")


class Habitacion(ElementoMapa):
    """
    Equivale a la clase Habitacion, que en Smalltalk heredaba de Contenedor
    pero aquí la simplificamos con referencias directas.
    """
    def __init__(self, num):
        self.num = num
        self.norte = None
        self.sur = None
        self.este = None
        self.oeste = None
    
    def es_habitacion(self):
        return True

    def conectar(self, direccion, elemento):
        """
        Conecta (establece) el 'elemento' (Puerta, Pared, etc.) en
        la dirección dada ('norte', 'sur', 'este' o 'oeste').
        """
        setattr(self, direccion, elemento)


class Laberinto(ElementoMapa):
    """
    Equivale a la clase Laberinto, que en Smalltalk era un Contenedor
    de habitaciones.
    """
    def __init__(self):
        self.habitaciones = []
    
    def agregar_habitacion(self, habitacion):
        self.habitaciones.append(habitacion)
    
    def obtener_habitacion(self, num):
        return next((hab for hab in self.habitaciones if hab.num == num), None)
    
    def entrar(self):
        # En Smalltalk quedaba sin definir (o vacío).
        # Aquí, si quisiéramos, podríamos simular "entrar en la hab.1".
        pass


class Modo:
    """
    Equivale a la clase abstracta Modo en Smalltalk, con
    actua:unBicho, camina:unBicho, esAgresivo, esPerezoso...
    """
    def actua(self, bicho):
        # Template Method
        self.camina(bicho)

    def camina(self, bicho):
        # En Smalltalk: self subclassResponsibility
        raise NotImplementedError("Debe implementarse en subclases")
    
    def es_agresivo(self):
        return False
    
    def es_perezoso(self):
        return False


class Agresivo(Modo):
    def es_agresivo(self):
        return True

    # Si quisieras algún comportamiento concreto de moverse:
    # def camina(self, bicho):
    #     print("El bicho agresivo avanza rápido")


class Perezoso(Modo):
    def es_perezoso(self):
        return True

    # def camina(self, bicho):
    #     print("El bicho perezoso se mueve lento")


class Bicho:
    """
    Equivale a la clase Bicho.
    Tiene vidas, poder, modo (agresivo o perezoso) y posición (Habitacion).
    """
    def __init__(self):
        self.vidas = 5
        self.poder = 1
        self.modo = None
        self.posicion = None
    
    def actua(self):
        # delega en el modo
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


class Juego:
    """
    Equivale a la clase Juego, que en Smalltalk maneja el laberinto y los bichos.
    """
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
    
    def obtener_habitacion(self, num):
        """
        Equivale a:
        ^ self laberinto obtenerHabitacion: unNum
        """
        return self.laberinto.obtener_habitacion(num)

    # ---------------------------------------------------------------------
    # Métodos para crear distintos laberintos, equivalentes al Smalltalk.
    # ---------------------------------------------------------------------

    def crear_laberinto_2_habitaciones(self):
        """
        Equivale a Juego>>crearLaberinto2Habitaciones
        Crea 2 habitaciones con sus paredes y una puerta que las conecta.
        """
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
        """
        Equivale a Juego>>crearLaberinto2HabitacionesFM:
        Crea 2 habitaciones usando un Creator (Factory Method),
        y conecta con una puerta entre sur y norte.
        """
        hab1 = creator.fabricar_habitacion(1)
        hab2 = creator.fabricar_habitacion(2)

        # Puerta "fabricada" por el Creator (requiere lado1, lado2)
        puerta = creator.fabricar_puerta(hab1, hab2)

        # En Smalltalk, usaban orientaciones (sur/norte).
        # Aquí, lo hacemos directo:
        hab1.sur = puerta
        hab2.norte = puerta

        self.laberinto = creator.fabricar_laberinto()
        self.laberinto.agregar_habitacion(hab1)
        self.laberinto.agregar_habitacion(hab2)

        return self.laberinto

    def crear_laberinto_2_habitaciones_fmd(self, creator):
        """
        Equivale a Juego>>crearLaberinto2HabitacionesFMD:
        Parecido al anterior, pero además usa 'bomba' como decorador en el este de cada habitación.
        """
        hab1 = creator.fabricar_habitacion(1)
        hab2 = creator.fabricar_habitacion(2)

        # Creamos bombas y les asignamos una pared interna:
        bomba1 = creator.fabricar_bomba()
        bomba1.em = creator.fabricar_pared()
        hab1.este = bomba1

        bomba2 = creator.fabricar_bomba()
        bomba2.em = creator.fabricar_pared()
        hab2.este = bomba2

        # Creamos la puerta
        puerta = creator.fabricar_puerta(hab1, hab2)

        hab1.sur = puerta
        hab2.norte = puerta

        self.laberinto = creator.fabricar_laberinto()
        self.laberinto.agregar_habitacion(hab1)
        self.laberinto.agregar_habitacion(hab2)

        return self.laberinto

    def crear_laberinto_4_habitaciones(self):
        """
        Equivale a Juego>>crearLaberinto4Habitaciones en Smalltalk,
        con 4 habitaciones, 4 puertas y 4 bichos (2 rojos agresivos, 2 verdes perezosos).
        """
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
        bicho_rojo2.posicion = hab2  # Para ser fieles al Smalltalk (hab2)

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


class Creator:
    """
    Equivale a la clase Creator en Smalltalk.
    Por defecto crea Pared normal, etc.
    """
    def fabricar_habitacion(self, num):
        hab = Habitacion(num)
        # En la versión Smalltalk, se añadían orientaciones y se "forzaba"
        # a cada lado a ser una pared. Haremos lo equivalente:
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
    
    # En Smalltalk había "fabricarBomba". Lo añadimos también:
    def fabricar_bomba(self):
        # Crea una Bomba decorador sin 'em' al principio.
        return Bomba(None)

    # Métodos para crear bichos con modos (opcional, según se necesite):
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
