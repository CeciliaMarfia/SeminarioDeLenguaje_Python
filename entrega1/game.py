import random

# Lista de palabras posibles 
words = ["python", "programación", "computadora", "código", "desarrollo", 
"inteligencia"]

# Elegir una palabra al azar 
secret_word = random.choice(words)
 
# Número máximo de intentos permitidos
max_failures = 10
# Lista para almacenar las letras adivinadas 
guessed_letters = []
print("¡Bienvenido al juego de adivinanzas!")
print("Estoy pensando en una palabra. ¿Puedes adivinar cuál es?")

#Pedir al jugador que seleccione un nivel de dificultad
difficulty = input("Selecciona un nivel de dificultad (FÁCIL/MEDIA/DIFÍCIL): ").lower()

#Fácil: En la palabra a adivinar se muestran todas las vocales por defecto.
vowels = ['a', 'á' , 'e', 'é' ,'i','í' , 'o', 'ó', 'u', 'ú'] 
if difficulty == "fácil":
    word_displayed = ""

    for letter in secret_word:
        if letter.lower() in vowels:
            word_displayed += letter
        else:
            word_displayed += "_"

#Media: Se muestra la primer y la última letra de la palabra.
elif difficulty == "media":
    #word_displayed = secret_word[0] + "_" * (len(secret_word) - 2) + secret_word[-1]

    # Mostrar la palabra parcialmente adivinada
    letters = []
    guessed_letters.append(secret_word[0])
    guessed_letters.append(secret_word[-1])
    for letter in secret_word:
        if letter in guessed_letters:
            letters.append(letter)
        else:
            letters.append("_")
        word_displayed = "".join(letters)
#(len(secret_word) - 2) + secret_word[-1]  calcula la longitud de la palabra secreta (secret_word) y luego le resta 2 
#para saber la cantidad de guiones bajos que se deben agregar entre la primera letra y la última letra de la palabra

#Difícil: No se muestra ninguna letra de la palabra.
elif difficulty == "difícil":
    word_displayed = "_" * len(secret_word)

else:
    print("No has seleccionado nivel de dificultad")

# Mostrarla palabra parcialmente adivinada 
print(f"Palabra: {word_displayed}")

# Agregar las letras reveladas según el nivel de dificultad
letters_revealed = []
if difficulty == "fácil":
    for letter in secret_word:
        if letter.lower() in vowels:
            letters_revealed.append(letter)
elif difficulty == "media":
    letters_revealed.append(secret_word[0])
    letters_revealed.append(secret_word[-1])

guessed_letters.extend(letters_revealed)
#Inicializar el contador de fallos 
failures = 0
#Cortará cuando max_failures alcanza a failures
while failures < max_failures:
     # Pedir al jugador que ingrese una letra
    letter = input("Ingresa una letra: ").lower()

    #Verificar si se ha ingresado una letra
    if not letter.isalpha():
    #en el inciso anterior se ve que al guardar había olvidado los ()!!
        print("Error, por favor ingresa una letra.")
        failures+=1
        continue

    # Verificar si la letra ya ha sido adivinada
    if letter in guessed_letters:
        print("Ya has intentado con esa letra. Intenta con otra.")
        failures+=1
        continue

    # Agregar la letra a la lista de letras adivinadas
    guessed_letters.append(letter) 
    # Verificar si la letra está en la palabra secreta
    if letter in secret_word:
        print("¡Bien hecho! La letra está en la palabra.")
    else:
        print("Lo siento, la letra no está en la palabra.")
    
    #Incremento el contador de fallos
        failures+=1
 
    # Mostrar la palabra parcialmente adivinada
    letters = []
    for letter in secret_word:
        if letter in guessed_letters:
            letters.append(letter)
        else:
            letters.append("_")
    word_displayed = "".join(letters)
    print(f"Palabra: {word_displayed}")

    # Verificar si se ha adivinado la palabra completa
    if word_displayed == secret_word:
        print(f"¡Felicidades! Has adivinado la palabra secreta: {secret_word}")
        break

#En caso de alcanzar la cantidad de fallos se imprime en pantalla un cartel para dar aviso del mismo.
else:
        print(f"¡Oh no! Has agotado tus {max_failures} intentos.")
        print(f"La palabra secreta era: {secret_word}")