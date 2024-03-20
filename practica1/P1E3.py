""""
Crea un programa que calcule la suma de los primeros 100 números naturales
utilizando un bucle for.
"""
#Inicialización de la variable suma en cero
suma = int(0)
#Bucle for que va en el rango de 1 a 100
for i in range(1,101):
    #Sumo el valor anterior al actual
    suma = suma + i
#Muestro en pantalla el resultado
print("La suma total es: ", suma)