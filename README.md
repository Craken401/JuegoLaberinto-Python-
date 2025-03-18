# 🏰 Juego del Laberinto en Python

Este repositorio contiene la versión en **Python** del **Juego del Laberinto**, una adaptación fiel de la implementación original en **Smalltalk**.  
A lo largo de este proyecto se han aplicado varios **patrones de diseño** (*Factory Method*, *Decorator* y *Strategy*), manteniendo así una arquitectura **modular**, **flexible** y **mantenible**.

---

## 🌐 Diagrama UML Actualizado

A continuación se muestra un **diagrama UML** (colócalo en tu repositorio) donde se aprecian las clases principales (`Juego`, `Laberinto`, `Habitacion`, `Puerta`, `Pared`, `Bomba`, `Bicho`, `Personaje`, etc.) y sus relaciones:

> **![image](https://github.com/user-attachments/assets/146cfd55-c57f-4fd4-914c-4f6c5bae149d)**

---

## 📌 Estructura del Proyecto

### Clases Principales

- **`Juego`**  
  - Mantiene una instancia de `Laberinto` y referencias a una lista de `Bicho` (enemigos) y a un `Personaje`.
  - Proporciona métodos para construir laberintos de distinta complejidad:  
    - `crear_laberinto_2_habitaciones()`  
    - `crear_laberinto_4_habitaciones()`  
    - `crear_laberinto_2_habitaciones_fm(...)` (usa un `Creator` para el *Factory Method*).  
    - `crear_laberinto_2_habitaciones_fmd(...)` (combina *Factory Method* y *Decorator* para bombas).  
  - Incluye operaciones para `abrir_puertas()`, `cerrar_puertas()`, **lanzar** los bichos en hilos (`lanzar_bichos`) y manejar la lógica de “fin de juego”.
  - Ofrece métodos para **agregar** un personaje (`agregar_personaje(nombre)`) y para moverlo (`mover_personaje_hacia(orientacion)`).

- **`Laberinto`**  
  - Contiene una colección de `Habitacion`.
  - Permite **agregar** y **obtener** habitaciones.
  - Su método `entrar(bicho)` coloca el bicho en la **Habitación #1** (si existe).

- **`Habitacion`**  
  - Representa cada sala del laberinto, con cuatro direcciones (`norte`, `sur`, `este`, `oeste`).
  - Al `entrar(bicho)`, actualiza la posición del bicho y muestra un mensaje por consola.
  - Subclase especial: **`Armario`**, donde el personaje puede “esconderse”.

- **`ElementoMapa`** (superclase abstracta)  
  - Clase base para `Habitacion`, `Puerta`, `Pared`, `Bomba`, etc.
  - Métodos de consulta: `es_habitacion()`, `es_puerta()`, `es_pared()`.  
  - `entrar(bicho)` para manejar la interacción, y `recorrer(funcion)` para aplicar una función a sí mismo (y a sus hijos, en caso de contenerlos).

- **`Puerta`**  
  - Conecta dos habitaciones (`lado1`, `lado2`), con un estado `abierta/cerrada`.
  - `entrar(bicho)` decide hacia qué lado mover al bicho si la puerta está abierta, o avisa de que está cerrada.
  - `abrir()` y `cerrar()` muestran mensajes en consola.

- **`Pared`** y **`ParedBomba`**  
  - Simulan muros. Al chocar, muestran un mensaje.  
  - `ParedBomba` tiene una variable `activa` para comportamientos adicionales al chocar.

- **`Bomba`** (Decorator)  
  - Clase que envuelve otro `ElementoMapa` (por ejemplo, una `Pared`) y añade el comportamiento adicional de explotar o mostrar un mensaje si `activa=True`.

- **`Personaje`**  
  - Subclase de `Ente`. Atributo `nombre`, además de los heredados (`vidas`, `poder`, `posicion`, etc.).
  - Métodos como:
    - `atacar()`: ataca a todos los bichos en la misma habitación (internamente llama a métodos del `Juego`).
    - `caminar_hacia(orientacion)`: mover al personaje por el laberinto (Norte, Sur, Este, Oeste).
  - Si sus `vidas` llegan a 0, se considera que “ganan los bichos” y se termina el juego.

- **`Bicho`**  
  - Otro heredero de `Ente`, representa criaturas hostiles.
  - Tiene un `modo` (estrategia) que puede ser `Agresivo` o `Perezoso`.
  - Método `actua()`: duerme un tiempo, camina y ataca (según su *Strategy*).
  - Cuando muere (`vidas`=0), avisa al `Juego` que revisa si todos los bichos están muertos y, de ser así, el personaje gana.

### Orientaciones

- **`Norte`**, `Sur`, `Este`, `Oeste`  
  - Clases que podrían llamarse “Orientación”: proporcionan métodos para `caminar(bicho)` en una dirección concreta (delegación).

### Patrones de Diseño

1. **Factory Method**  
   - Clases `Creator` y `CreatorB`.
   - Permite personalizar qué tipo de paredes, puertas, bombas, etc., se instancian al construir el laberinto.
2. **Decorator**  
   - La clase `Bomba` (o `ParedBomba`) extiende el comportamiento de otro `ElementoMapa`.
   - Añade efectos sin modificar la clase base.
3. **Strategy**  
   - Cada `Bicho` se asocia a un `modo` (`Agresivo` o `Perezoso`), el cual define su forma de dormir, atacar y moverse.  
   - Permite cambiar el comportamiento en tiempo de ejecución.

---

## 🏗 Director y LaberintoBuilder (Construcción desde JSON)

- **`LaberintoBuilder`**  
  - Se encarga de *fabricar* las habitaciones, bombas, etc.  
  - Permite luego construir un `Juego` con su `laberinto` asociado.
- **`Director`**  
  - Lee un archivo JSON (usando el módulo `json` en Python).
  - Aplica un `builder` para crear el laberinto (llamando a `fabricar_habitacion`, `fabricar_bomba_en`, etc.).
  - Después fabrica el `Juego` y los bichos (si en el JSON se define `"bichos"`).
  - Método principal: `procesar(ruta_de_json)`, que ejecuta:
    1. `leer_archivo(...)`
    2. `ini_builder()`
    3. `fabricarLaberinto()`
    4. `fabricarJuego()`
    5. `fabricarBichos()`
  - Devuelve el `Juego` con `obtener_juego()`.

Esta parte equivale a lo que en Smalltalk se hacía con `Director`, `LaberintoBuilder` y `NeoJSONReader`.

---

## 🚀 Ejecución y Uso

### 1. Clona este repositorio

```bash
git clone https://github.com/tu-usuario/laberinto-python.git
cd laberinto-python
```
2. Verifica que tienes Python 3 instalado
   python --version
3. Ejecución de ejemplo
   Crea o edita un archivo main.py (o usa un intérprete interactivo):

from director import Director
from juego import Juego, Creator, CreatorB

# Usar Director para JSON
director = Director()
director.procesar("lab2Hab1Bomba.json")  # ejemplo de JSON con bichos y bombas
juego = director.obtener_juego()

# Agregamos un personaje y lo movemos
juego.agregar_personaje("Pepe")
juego.abrir_puertas()
juego.lanzar_bichos()

# También puedes usar los métodos directos de 'Juego' y 'Creator'
juego2 = Juego()
creator = Creator()
juego2.crear_laberinto_2_habitaciones_fm(creator)
juego2.agregar_personaje("Juan")
juego2.abrir_puertas()


Luego ejecuta: python main.py
Verás en la salida mensajes sobre la creación de habitaciones, apertura de puertas, movimientos de bichos, etc.

Métodos Destacados
Juego.crear_laberinto_2_habitaciones()
Construye un laberinto pequeño con dos salas unidas por una puerta.

Juego.crear_laberinto_4_habitaciones()
Crea un laberinto más grande con 4 habitaciones y 4 bichos (2 agresivos y 2 perezosos).

Juego.crear_laberinto_2_habitaciones_fm(creator)
Usa un Creator para fabricar las habitaciones, puertas y paredes (ejemplo de Factory Method).

Juego.crear_laberinto_2_habitaciones_fmd(creator)
Similar al anterior, pero incluye “bombas” como Decorators.

Juego.abrir_puertas() / Juego.cerrar_puertas()
Recorren el laberinto llamando a abrir() o cerrar() en cada Puerta.

Juego.lanzar_bichos()
Inicia un hilo por cada Bicho, para que se muevan y ataquen concurrentemente.

Personaje.atacar()
Ataca a todos los bichos en la misma habitación (gestiona internamente la lógica en Juego).

Personaje.caminar_hacia(orientacion)
Mueve al personaje en la dirección especificada (Norte, Sur, Este, Oeste).

Bicho.actua()
Llama a su modo (Agresivo o Perezoso) para “dormir” primero, luego “caminar” y finalmente “atacar”.


Autor:
Víctor Nolasco Sánchez
[GitHub](https://github.com/Craken401)

¡Gracias por visitar este repositorio!
Cualquier sugerencia o mejora es bienvenida.
Si te resulta útil, no olvides dejar una ⭐ en GitHub.
