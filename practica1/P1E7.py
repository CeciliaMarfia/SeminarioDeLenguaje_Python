""""
7. Escribe un programa que tome una lista de números enteros 
como entrada del usuario. Luego, convierte cada número en la lista a
string y únelos en una sola cadena, separados por guiones ('-'). 
Sin embargo, excluye cualquier número que sea múltiplo de 3 de la cadena final.
"""
#Creación de la lista
lista = []
#Solicito al usuario que ingrese una lista de números
while True:
    numero = int(input("Ingresa un número para generar la lista (ingresa 0 para terminar): "))
    if numero != 0:
        lista.append(numero)
    else:
        break
cadena =""
  
for numero in lista:    
    if numero % 3 != 0:
        cadena += str(numero) + "-"
    cadena=cadena[:-1]
print("Cadena final: ", cadena)