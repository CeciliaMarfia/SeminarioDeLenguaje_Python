""""
5. Implementa un programa que solicite al usuario que ingrese una 
lista de números. 
Luego, imprime la lista pero detén la impresión 
si encuentras un número negativo. Nota: utilice la sentencia break 
cuando haga falta.
"""
#Creación de la lista
lista = []
#Solicito al usuario que ingrese una lista de números
while True:
    numero = int(input("Ingresa un número para generar la lista (ingresa 0 para terminar): "))
    if numero == 0:
        break
    lista.append(numero)
# Imprimir la lista de números ingresada por el usuario pero detén la impresión 
#si encuentras un número negativo
for numero in lista:
    if (numero < 0):
        break
    print(numero)
print("Lista de números ingresada:", lista)