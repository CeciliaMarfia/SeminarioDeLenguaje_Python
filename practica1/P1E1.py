
""""
1. Desarrolla un programa que solicite al usuario que ingrese su edad y 
luego calcule y muestre cuántos años le faltan para alcanzar los 100 años.
"""
# Solicito la edad al usuario
# en la variable edad voy a almacenar un valor entero y utilizo input() para leer el dato, todo lo que yo lea en python se lee como string
edad = int(input("Por favor, ingresa tu edad: "))

if edad > 0:
    # Calcular cuántos años faltan para alcanzar los 100 años
    anios_para_100 = 100 - edad

    # Mostrar el resultado
    print(f"los años que te faltan para llegar a 100 es: {100-edad}")
else:
    if edad == 0:
        print("¡Ya tienes 100 años!")
    else:
        print('Ingresaste una edad negativa')