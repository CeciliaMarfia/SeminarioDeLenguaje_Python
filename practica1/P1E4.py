""""
4. Cree un programa que dada una lista de números imprima sólo los que 
son pares. Nota: utilice la sentencia continue donde haga falta.
"""
# Definir una lista de números
numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# Iterar sobre la lista
""""
En Python, cuando utilizas un bucle for, la variable que usas para iterar 
(en este caso, numero) toma el valor del primer elemento de la secuencia 
sobre la que estás iterando en la primera iteración del bucle.
"""
for numero in numeros:
    if numero % 2 != 0:
    # Si es impar, pasar a la siguiente iteración
        continue
    # Si es par, imprimirlo
    print(numero)