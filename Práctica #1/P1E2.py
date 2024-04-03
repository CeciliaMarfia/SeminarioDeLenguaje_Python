""""
2. Haz un programa que pida al usuario que ingrese una temperatura 
en grados Celsius y luego convierta esa temperatura a grados Fahrenheit,
mostrando el resultado.
"""
#Solicito al usuario ingresar la temperatura en grados Celsius
temperatura = float(input("Ingrese una temperatura en grados Celsius:"))

#Realizo la conversión

farenheit =  (temperatura * 9/5)+32

#Imprimo el resultado

print(temperatura," grados Celsius en Farenheit es: ",farenheit)