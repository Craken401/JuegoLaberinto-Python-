from main import Director, Sur, Norte, Este, Oeste
import os
if __name__ == "__main__":
    # 1) Creamos un Director
    director = Director()

    # 2) Procesamos un archivo JSON (por ejemplo lab4Hab.json con 4 habitaciones y bichos)
    director.procesar("C:\\Users\\victo\\Desktop\\Proyecto Diseño Software Python\\laberintos\\lab4Hab.json")

    # 3) Obtenemos el 'Juego' ya construido
    juego = director.obtener_juego()

    # 4) Creamos un personaje y lo añadimos al juego
    juego.agregar_personaje("Heroe")

    # 5) (Opcional) Abrimos las puertas, para que el personaje o los bichos se muevan fácilmente
    juego.abrir_puertas()

    # 6) Lanzamos los bichos en hilos, para que empiecen a actuar
    juego.lanzar_bichos()

while True:
    comando = input("Movimiento (w=arriba, s=abajo, a=izq, d=der, x=salir): ")
    if comando == 'w':
        juego.mover_personaje_hacia(Norte())
    elif comando == 's':
        juego.mover_personaje_hacia(Sur())
    elif comando == 'a':
        juego.mover_personaje_hacia(Oeste())
    elif comando == 'd':
        juego.mover_personaje_hacia(Este())
    elif comando == 'x':
        print("Saliendo...")
        break
    else:
        print("Comando no reconocido.")
    
    # Podrías llamar a juego.person.atacar() después de cada movimiento, etc.


    # 7) Hacemos movimientos del personaje “a mano”
    #    Por ejemplo, mover el personaje hacia el Sur, Norte, Este, Oeste
    juego.mover_personaje_hacia(Sur())   # mueve personaje Sur
    juego.mover_personaje_hacia(Este())  # luego Este
    # ...
    
    # 8) Atacamos (por si algún bicho está en la misma habitación):
    juego.person.atacar()

    # 9) Si quieres, duermes un tiempo para ver cómo atacan los bichos
    import time
    time.sleep(5)  # duerme 5 segundos

    # 10) Cerrar el programa: terminarBichos (para que mueran y acaben los hilos)
    juego.terminar_bichos()

    print("Fin de la demo.")
