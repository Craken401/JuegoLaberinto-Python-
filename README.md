# 🏰 Juego del Laberinto en Python

Este repositorio contiene la versión en **Python** del **Juego del Laberinto**, una adaptación de la implementación original en Smalltalk. En este proyecto, se han aplicado patrones de diseño para garantizar una estructura modular, flexible y mantenible.

## 📌 Estructura del Proyecto

Las clases principales del juego son:

- **`Juego`**: Contiene la instancia de `Laberinto` y gestiona los `Bichos`.
- **`Laberinto`**: Contiene una colección de habitaciones (`Habitacion`).
- **`Habitacion`**: Define las habitaciones del laberinto con sus conexiones (`norte`, `sur`, `este`, `oeste`).
- **`ElementoMapa`**: Clase base para los elementos del laberinto (`Habitacion`, `Puerta`, `Pared`).
- **`Puerta`**: Conecta dos habitaciones y puede estar abierta o cerrada.
- **`Pared`**: Representa los muros del laberinto.
- **`ParedBomba`**: Subclase de `Pared` que explota si está activada.
- **`Bicho`**: Representa enemigos en el laberinto, pudiendo ser `Agresivo` o `Perezoso`.

---

## 🏛 Patrones de Diseño Implementados

### 🔨 Factory Method
- Implementado en `Creator`, que permite fabricar distintos elementos (`Habitacion`, `Pared`, `Puerta`).
- También existe `CreatorB`, que genera **paredes con bombas** en lugar de paredes normales.

### 🎭 Decorator
- Implementado en `ParedBomba`, que actúa como un **decorador** de `Pared`.

### ♟️ Strategy
- Implementado con `Modo`, que define la estrategia de comportamiento de los `Bichos` (`Agresivo` o `Perezoso`).

---

## 🚀 Cómo Ejecutarlo

1. Clonar este repositorio.
2. Asegurarse de tener **Python 3.x** instalado.
3. Ejecutar el archivo `main.py`:

```python
from juego import Juego

juego = Juego()
laberinto = juego.laberinto
print("Laberinto generado con éxito")

