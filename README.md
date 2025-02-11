# 🏰 Juego del Laberinto WIP (Work In Progress) en Python.

Este repositorio es la versión en **Python** del **Juego del Laberinto**, originalmente implementado en Smalltalk. Se han mantenido las estructuras y patrones de diseño utilizados en la versión original de SmallTalk.

## 📌 Estructura del Proyecto

Las clases principales del juego son:

- **`Juego`**: Contiene una instancia de `Laberinto`.
- **`Laberinto`**: Colección de habitaciones (`Habitacion`).
- **`Habitacion`**: Contiene información sobre sus conexiones (`norte`, `sur`, `este`, `oeste`).
- **`ElementoMapa`**: Clase base para todos los elementos del laberinto.
- **`Pared`**: Representa los muros dentro del laberinto.
- **`Puerta`**: Conecta dos habitaciones y puede estar abierta o cerrada.

---

## 🏛 Patrones de Diseño Implementados

### 🔨 Factory Method
- Implementado en `Creator` para la generación de habitaciones, paredes y puertas.
- Mejora la flexibilidad y modularidad del código.

### 🎭 Decorator
- **`Hechizo`** permite aplicar encantamientos a `Puerta` y `Habitacion`.
- No modifica la estructura base de las clases decoradas.

### ♟️ Strategy
- **`EstrategiaMovimiento`** define distintas formas de recorrer el laberinto.
- Permite cambiar la estrategia en tiempo de ejecución.

---

## 🚀 Cómo Ejecutarlo

1. Clonar este repositorio.
2. Asegurarse de tener Python instalado (versión 3.x).
3. Ejecutar el archivo `main.py`.

```python
from juego import Juego

juego = Juego()
laberinto = juego.laberinto
print("Laberinto generado con éxito")
