# 🏰 Juego del Laberinto en Python

Este repositorio contiene la versión en **Python** del **Juego del Laberinto**, una adaptación de la implementación original en Smalltalk. A lo largo de este proyecto se han aplicado varios **patrones de diseño** (*Factory Method*, *Decorator*, *Strategy*), lo que garantiza una estructura **modular**, **flexible** y **mantenible**.

---

![image](https://github.com/user-attachments/assets/f5fa1baf-3b58-40ac-b063-946f0bac3f6b)


## 📌 Estructura del Proyecto

Las **clases principales** del juego son:

- **`Juego`**  
  - Mantiene una instancia de `Laberinto` y varias referencias a `Bicho`.
  - Proporciona métodos para crear laberintos de diferente complejidad (2 habitaciones, 4 habitaciones, con bombas, etc.).
  - Añade funciones para abrir/cerrar puertas, lanzar los bichos en hilos, etc.

- **`Laberinto`**  
  - Contiene una colección de `Habitacion`.
  - Permite **agregar** y **obtener** habitaciones.
  - Ofrece un método `entrar(bicho)` para situar el bicho en la **Habitación #1**.

- **`Habitacion`**  
  - Define la estructura de cada sala del laberinto.
  - Dispone de atributos para las cuatro direcciones: `norte`, `sur`, `este`, `oeste`.
  - Su método `entrar(bicho)` sitúa al bicho dentro y muestra un mensaje en consola.

- **`ElementoMapa`** (superclase de todo)  
  - Clase base para todos los elementos del mapa: `Habitacion`, `Puerta`, `Pared`, etc.
  - Incluye métodos de consulta (`es_habitacion`, `es_puerta`, `es_pared`) y un método `entrar()` para gestionar la interacción.
  - Cada elemento puede, además, implementarse para *recorrer* (ver `recorrer(funcion)`).

- **`Puerta`**  
  - Conecta dos habitaciones (`lado1` y `lado2`).
  - Puede estar abierta o cerrada, y su `entrar(bicho)` decide a qué lado moverse.
  - Implementa métodos `abrir()` y `cerrar()` que muestran mensajes en la consola.

- **`Pared`** y **`ParedBomba`**  
  - Representan los muros del laberinto, con su comportamiento al “chocarse” el bicho.
  - `ParedBomba` es una subclase de `Pared` con la variable `activa` (permite simular explosiones).

- **`Bicho`**  
  - Representa a las criaturas/enemigos dentro del laberinto.
  - Atributos: `vidas`, `poder`, `posicion` y un `modo` (estrategia).
  - Puede “actuar” (`actua()`), lo que implica “caminar” y “atacar” según su modo.

- **`Modo`** (superclase)  
  - Define la **estrategia** de comportamiento de un `Bicho`.
  - Clases concretas: `Agresivo` y `Perezoso`, que implementan cómo “caminan” y “duermen”, etc.
  
- **`Creator`** y **`CreatorB`**  
  - Aplican el patrón *Factory Method* para instanciar elementos (`Habitacion`, `Pared`, `Puerta`, `Bomba`).
  - `CreatorB` es una variante que crea `ParedBomba` en lugar de `Pared` normal.

---

## 🏛 Patrones de Diseño Implementados

### 🔨 Factory Method
- Se concentra en las clases `Creator` y `CreatorB`.
- Permite “fabricar” distintas variantes de los elementos del laberinto:
  - Habitaciones, paredes normales o bombas, puertas, etc.

### 🎭 Decorator
- El decorador principal es la clase `Bomba`, que “envuelve” a otro elemento del mapa (por defecto, una pared).
- Permite añadir la funcionalidad de “bomba” (explosión o mensaje de choque) sin modificar la clase original.

### ♟️ Strategy
- Se ve reflejado en la jerarquía `Modo` (`Agresivo` y `Perezoso`).
- Cada `Bicho` delega parte de su comportamiento (caminar, dormir, atacar) al `modo`, cambiando así su estrategia de juego.

---

## 🚀 Ejecución y Uso

1. **Clonar el repositorio**  
   ```bash
   git clone https://github.com/tu-usuario/laberinto-python.git
   cd laberinto-python

2. Verificar instalación de Python 3
Asegúrate de que Python 3.x esté instalado:
python --version

3. Ejecutar o importar en tu proyecto
Puedes crear un archivo main.py para probar las clases y métodos. Ejemplo:

from juego import Juego, Creator, CreatorB

# Crear un juego y un Creator por defecto
juego = Juego()
creator = Creator()

# Crear un laberinto de 2 habitaciones normal
laberinto_simple = juego.crear_laberinto_2_habitaciones()

# Crear un laberinto de 4 habitaciones con bichos agresivos y perezosos
juego.crear_laberinto_4_habitaciones()
print("Habitaciones en el laberinto:", len(juego.laberinto.habitaciones))

# Crear un laberinto usando Factory Method para generar paredes bomba
juego2 = Juego()
creator_b = CreatorB()
laberinto_bombas = juego2.crear_laberinto_2_habitaciones_fmd(creator_b)
print("Laberinto con paredes bomba listo!")

4. Ejecuta el script:
python main.py
Verás mensajes sobre la creación de habitaciones, puertas, etc.

✨ Ejemplos de Métodos Disponibles
Dentro de la clase Juego, se incluyen varios métodos de construcción del laberinto:

crear_laberinto_2_habitaciones()
Crea un laberinto básico de 2 habitaciones con paredes simples y una sola puerta conectando.

crear_laberinto_2_habitaciones_fm(creator)
Utiliza un objeto Creator (o CreatorB) para fabricar las habitaciones y la puerta. Muestra el uso de Factory Method.

crear_laberinto_2_habitaciones_fmd(creator)
Añade bombas “decoradoras” en el este de cada habitación, usando el patrón Decorator.

crear_laberinto_4_habitaciones()
Construye un laberinto más grande con 4 habitaciones y 4 bichos (2 agresivos, 2 perezosos).

Además, existen métodos para abrirPuertas, cerrarPuertas, lanzarBichos, etc.

Autor:
Víctor Nolasco Sánchez
[GitHub](https://github.com/Craken401)

¡Gracias por visitar este repositorio!
Cualquier sugerencia o mejora es bienvenida.
Si te resulta útil, no olvides dejar una ⭐ en GitHub.
