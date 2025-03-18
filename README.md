# 🏰 Juego del Laberinto en Python

Este repositorio contiene la versión en **Python** del **Juego del Laberinto**, una adaptación fiel de la implementación original en **Smalltalk**.  
A lo largo de este proyecto se han aplicado varios **patrones de diseño** (*Factory Method*, *Decorator* y *Strategy*), manteniendo así una arquitectura **modular**, **flexible** y **mantenible**.

---

## 🌐 Diagrama UML Actualizado

A continuación se muestra el **diagrama UML** de la versión final, donde se aprecian las clases principales (`Juego`, `Laberinto`, `Habitacion`, `Puerta`, `Pared`, `Bomba`, `Bicho`, `Personaje`, etc.) y sus relaciones:

![image](https://github.com/user-attachments/assets/3cac78d3-ded1-40fa-a371-384485820a46)


> (Reemplaza la URL anterior con la ruta real de la imagen en tu repositorio, si procede.)

---

## 📌 Estructura del Proyecto

### Clases Principales

- **`Juego`**  
  - Mantiene una instancia de `Laberinto` y referencias a `Bicho` (enemigos) y a un `Personaje`.
  - Proporciona métodos para construir laberintos de distinta complejidad:  
    - `crear_laberinto_2_habitaciones()`  
    - `crear_laberinto_4_habitaciones()`  
    - `crear_laberinto_2_habitaciones_fm(...)` (usa un `Creator` para el *Factory Method*).  
    - `crear_laberinto_2_habitaciones_fmd(...)` (combina *Factory Method* y *Decorator* para bombas).  
  - Incluye operaciones para `abrir_puertas()`, `cerrar_puertas()`, **lanzar** los bichos en hilos (`lanzar_bichos`), y manejar la lógica de “fin de juego”.

- **`Laberinto`**  
  - Contiene una colección de `Habitacion`.
  - Permite **agregar** y **obtener** habitaciones.
  - Su método `entrar(bicho)` coloca el bicho en la **Habitación #1**.

- **`Habitacion`**  
  - Representa cada sala del laberinto, con sus cuatro direcciones (`norte`, `sur`, `este`, `oeste`).
  - Al `entrar(bicho)`, actualiza la posición del bicho y muestra un mensaje.

- **`ElementoMapa`** (superclase de todo)  
  - Clase base para `Habitacion`, `Puerta`, `Pared`, `Bomba`, etc.
  - Métodos de consulta: `es_habitacion()`, `es_puerta()`, `es_pared()`.  
  - `entrar(bicho)` para manejar la interacción, y `recorrer(funcion)` para iterar internamente.

- **`Puerta`**  
  - Conecta dos habitaciones (`lado1`, `lado2`), con estado `abierta/cerrada`.
  - `entrar(bicho)` decide hacia qué lado mover al bicho si la puerta está abierta.  
  - `abrir()` y `cerrar()` muestran mensajes de consola.

- **`Pared`** y **`ParedBomba`**  
  - Simulan muros. Al chocar, muestran un mensaje.  
  - `ParedBomba` tiene una variable `activa` que, de estar `True`, podría producir explosión o daño adicional.

- **`Personaje`**  
  - Ahora existe un “Personaje” (el usuario/jugador), subclase de `Ente`.
  - Atributo `nombre`, además de `vidas` y `poder` (heredados).
  - Métodos como `atacar()`, que ataca a todos los bichos en la misma habitación, y `caminar_hacia(unaOrientacion)` para moverse dentro del laberinto.
  - Si sus `vidas` llegan a 0, se considera que el juego termina (fin del juego: ganan los bichos).

- **`Bicho`**  
  - Representa a las criaturas hostiles.  
  - Atributos: `vidas`, `poder`, `posicion`, y un `modo` (la *Strategy*).
  - Método `actua()` que combina “dormir”, “caminar” y “atacar” (según su modo).
  - Cuando `vidas` llega a 0, se notifica al `Juego` para ver si el Personaje resulta ganador.

- **`Modo`** (superclase)  
  - *Strategy* para el comportamiento de `Bicho`.
  - Subclases: `Agresivo` y `Perezoso`, que redefinen `dormir`, `caminar` y `atacar`.
  - `Agresivo` descansa poco tiempo (1 segundo) y tiende a buscar al personaje rápido.
  - `Perezoso` duerme más (3 segundos) antes de moverse y atacar.

- **`Creator`** y **`CreatorB`**  
  - *Factory Method* para fabricar objetos del laberinto (`Habitacion`, `Pared`, `Puerta`, etc.).
  - `CreatorB` crea `ParedBomba` en lugar de `Pared` normal.
  - También pueden fabricar `Bomba` como *Decorator*.

---

## 🏛 Patrones de Diseño Implementados

1. **Factory Method**  
   - Clases `Creator` y `CreatorB`.
   - Permite personalizar qué tipo de paredes, bombas o puertas se instancian en la creación del laberinto.

2. **Decorator**  
   - La clase `Bomba` envuelve a otro `ElementoMapa` (por ejemplo, una `Pared`), añadiendo comportamiento extra (mensaje de explosión).
   - Extiende funcionalidad sin modificar la clase original.

3. **Strategy**  
   - Cada `Bicho` delega su comportamiento al `modo` (`Agresivo` o `Perezoso`).
   - El método `actua()` aplica la *estrategia* de movimiento, ataque y descanso.

---

## 🚀 Ejecución y Uso

1. **Clona este repositorio**  
   ```bash
   git clone https://github.com/tu-usuario/laberinto-python.git
   cd laberinto-python
2. Verifica que tienes Python 3 instalado
   python --version
3. Ejecutar o importar en tu proyecto
   Puedes crear un archivo main.py para hacer pruebas. Por ejemplo:

   from juego import Juego, Creator, CreatorB

# Crear un juego y su Creator por defecto
juego = Juego()
creator = Creator()

# Crear un laberinto de 2 habitaciones simple
laberinto_simple = juego.crear_laberinto_2_habitaciones()

# Crear un laberinto de 4 habitaciones con bichos
juego.crear_laberinto_4_habitaciones()
print("Habitaciones en el laberinto:", len(juego.laberinto.habitaciones))

# Probar Factory Method con paredes bomba
juego_bombas = Juego()
creator_b = CreatorB()
laberinto_con_bombas = juego_bombas.crear_laberinto_2_habitaciones_fmd(creator_b)
print("Laberinto con paredes bomba listo!")

4. Ejecución del script
python main.py

Verás en la salida mensajes sobre la creación de habitaciones, apertura y cierre de puertas, movimientos de bichos, etc.

Métodos Destacados
Juego.crear_laberinto_2_habitaciones()
Crea un laberinto pequeño con dos salas unidas por una puerta.

Juego.crear_laberinto_4_habitaciones()
Construye un laberinto más grande con 4 habitaciones y 4 bichos (2 agresivos, 2 perezosos).

Juego.crear_laberinto_2_habitaciones_fm(creator)
Usa un Creator para fabricar las habitaciones, puertas y paredes.
Muestra el uso del Factory Method.

Juego.crear_laberinto_2_habitaciones_fmd(creator)
Igual que el anterior, pero añade “bombas” como Decorators en algunas paredes.

Juego.abrir_puertas() / Juego.cerrar_puertas()
Recorren el laberinto llamando a abrir() o cerrar() en cada Puerta.

Juego.lanzar_bichos()
Inicia un thread por cada bicho para que se muevan y ataquen de forma concurrente.

Personaje

atacar(): ataca a todos los bichos que estén en la misma habitación (internamente llama a métodos del Juego para identificarlos).
caminar_hacia(orientacion): mueve al personaje en la dirección indicada (Norte, Sur, Este, Oeste).
Bicho.actua()

Llama a su modo (Agresivo / Perezoso) para “dormir” primero, luego “caminar” y finalmente “atacar”.
El “ataque” busca al Personaje en la misma habitación, reduciendo sus vidas si lo encuentra.


Autor:
Víctor Nolasco Sánchez
[GitHub](https://github.com/Craken401)

¡Gracias por visitar este repositorio!
Cualquier sugerencia o mejora es bienvenida.
Si te resulta útil, no olvides dejar una ⭐ en GitHub.
