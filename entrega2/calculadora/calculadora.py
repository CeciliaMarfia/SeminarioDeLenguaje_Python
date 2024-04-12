def statistics_generator(names, goals, goals_avoided, assists):
    """Genera una estructura de estadísticas para cada jugador. 
La función retorna una lista de diccionarios, donde cada diccionario representa las estadísticas de un jugador."""
    
    if len(names) == len(goals) == len(goals_avoided) == len(assists):
        statistics = []
        for i in range(len(names)):
            player = {
                "Nombre": names[i],
                "Goles a favor": goals[i],
                "Goles evitados": goals_avoided[i],
                "Asistencias": assists[i]
            }
            statistics.append(player)
        return statistics
    else:
         print("Error: las listas de datos son de diferente longitud")
         return None


def top_scorer(statistics):
    """ Encuentra al máximo goleador del equipo.
Retorna Una tupla que contiene el nombre y la cantidad de goles del máximo goleador."""
   
    max_goals_player = max(statistics, key=lambda x: x["Goles a favor"])
    return (max_goals_player["Nombre"], max_goals_player["Goles a favor"])
 

def most_influential_player(statistics):
    """ Encuentra al jugador más influyente del equipo.
  Se retorna una tupla que contiene el nombre y el puntaje del jugador más influyente."""
    #almacenare un dato de tipo punto flotante en max_score con un valor bajo.
    max_score = float(-1)
    influential_player = ""
    for player in statistics:
        score = player["Goles a favor"] * 1.5 + player["Goles evitados"] * 1.25 + player["Asistencias"]
        if score > max_score:
            max_score = score
            influential_player = player["Nombre"]
    return influential_player, max_score

def averaging(total_goals,games):
    """ Calcula el promedio de una cantidad total de goles en función de la cantidad de partidos jugados.
 Retorna el promedio de goles por partido."""
    average = total_goals/games
    return average


def average_best_player(maxGoals,games):
    """ Calcula el promedio de goles por partido del mejor jugador.
Nos retorna el promedio de goles por partido del mejor jugador. """
    result = float (maxGoals/games)
    return result