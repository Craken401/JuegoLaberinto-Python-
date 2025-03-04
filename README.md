# 🏰 Juego del Laberinto en Python

Este repositorio contiene la versión en **Python** del **Juego del Laberinto**, una adaptación de la implementación original en Smalltalk. En este proyecto, se han aplicado varios patrones de diseño para garantizar una estructura modular, flexible y mantenible.

![image](https://github.com/user-attachments/assets/00211d76-6e7c-4be7-be81-b9b1e3af8a74)


---

## 📌 Estructura del Proyecto

Las clases principales del juego son:

- **`Juego`**  
  - Mantiene una instancia de `Laberinto` y gestiona los `Bicho`.
  - Proporciona métodos para crear laberintos de diferente complejidad (2 habitaciones, 4 habitaciones, con bombas, etc.).

- **`Laberinto`**  
  - Contiene una colección de habitaciones (`Habitacion`).
  - Permite agregar y obtener habitaciones.

- **`Habitacion`**  
  - Define la estructura de cada sala del laberinto.
  - Dispone de conexiones para las cuatro direcciones: `norte`, `sur`, `este`, `oeste`.

- **`ElementoMapa`**  
  - Clase base para todos los elementos del mapa: `Habitacion`, `Puerta`, `Pared`, etc.
  - Incluye métodos de consulta (`es_habitacion`, `es_puerta`, `es_pared`) y un método `entrar()` para simular la interacción.

- **`Puerta`**  
  - Une dos habitaciones y puede estar abierta o cerrada.
  - Su método `entrar()` indica si está abierta o cerrada.

- **`Pared`**  
  - Representa un simple muro dentro del laberinto.

- **`ParedBomba`** (subclase de `Pared`)  
  - Actúa como un muro que puede explotar si está activado.
  - En este proyecto, simplemente muestra un mensaje al “chocarse” con ella.

- **`Bicho`**  
  - Representa los enemigos o criaturas dentro del laberinto.
  - Tiene atributos como `vidas`, `poder` y un `modo` (agresivo o perezoso).
  - Puede ubicarse en una determinada `Habitacion`.

- **`Modo`** (superclase)  
  - Define la estrategia de comportamiento de los `Bichos`.
  - Clases concretas: `Agresivo` y `Perezoso`, que implementan cómo se “mueven” o “actúan”.

- **`Creator`**  
  - Aplica el patrón *Factory Method* para instanciar elementos como `Habitacion`, `Pared`, `Puerta` y `Bomba`.
  - `CreatorB` es una variante que crea `ParedBomba` en vez de `Pared`.

---

## 🏛 Patrones de Diseño Implementados

### 🔨 Factory Method
- Se concentra en las clases `Creator` y `CreatorB`.
- Permite “fabricar” distintas variantes de los elementos del laberinto:
  - *Crea* `Habitacion`, `Pared`, `Puerta`, etc. con configuraciones distintas (por ejemplo, paredes bomba).

### 🎭 Decorator
- El decorador principal es la clase `Bomba`, que extiende la funcionalidad de otro elemento (`Pared` u otro `ElementoMapa`).
- Permite añadir comportamiento (mostrar un mensaje de explosión) sin modificar la clase original.

### ♟️ Strategy
- Se ve reflejado en la jerarquía `Modo` (`Agresivo` y `Perezoso`).
- Cada `Bicho` delega su comportamiento al `modo` para definir cómo “actúa” o “camina”.

---

## 🚀 Ejecución y Uso

1. **Clonar el repositorio**  
   ```bash
   git clone https://github.com/tu-usuario/laberinto-python.git
   cd laberinto-python
Verificar instalación de Python 3
Asegúrate de que Python 3.x esté correctamente instalado en tu sistema:

bash
Copiar
Editar
python --version
Ejecutar o importar en tu proyecto
Puedes crear un archivo main.py para probar las clases y métodos. Por ejemplo:

python
Copiar
Editar
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
Ejecuta el script:

bash
Copiar
Editar
python main.py
Verás en la salida mensajes sobre las creaciones de habitaciones, puertas, etc.

✨ Ejemplos de Métodos Disponibles
Dentro de la clase Juego, se incluyen varios métodos que ilustran distintas configuraciones del laberinto:

crear_laberinto_2_habitaciones()
Crea un laberinto básico de 2 habitaciones, con paredes simples y una puerta que las conecta.

crear_laberinto_2_habitaciones_fm(creator)
Utiliza un objeto Creator (o CreatorB) para fabricar las habitaciones y la puerta, ilustrando el uso del Factory Method.

crear_laberinto_2_habitaciones_fmd(creator)
Versión que añade bombas decoradoras en el este de cada habitación.

crear_laberinto_4_habitaciones()
Construye un laberinto más grande con 4 habitaciones y 4 bichos (2 agresivos y 2 perezosos).

⏳ Estado y Futuras Mejoras
Actualmente, el proyecto se centra en mostrar cómo se pueden modelar salas, puertas, paredes y bichos con diferentes comportamientos.
Se podrían añadir métodos que simulen el movimiento real de los bichos y sus interacciones más detalladas.
Integrar un sistema de pruebas con unittest o pytest para validar el comportamiento.
📄 Licencia
Este proyecto se distribuye bajo la MIT License. ¡Siéntete libre de usarlo, modificarlo y adaptarlo a tus necesidades!

Autor:
Víctor Nolasco Sánchez
[GitHub](https://github.com/Craken401)

¡Gracias por visitar este repositorio! Cualquier sugerencia o mejora es bienvenida.
Si te resulta útil, ¡no olvides dejar una ⭐ en GitHub!
