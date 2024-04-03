""""
6. Modifique el ejercicio 4 para que dada la lista de número genere 
dos nuevas listas, una con los número pares y otras con los que son impares.
Imprima las listas al terminar de procesarlas.
"""
# Definir una lista de números
numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print("La lista de números es: ", numeros)
listaPares = []
listaImpares =[]
for numero in numeros:
    if numero % 2 != 0:
    # Si es impar, lo agrego a la lista impar
        listaImpares.append(numero)
    else:
        # Si es par, lo agrego a la lista impar
        listaPares.append(numero)
print("Lista de números pares:", listaPares)
print("Lista de números impares:", listaImpares)