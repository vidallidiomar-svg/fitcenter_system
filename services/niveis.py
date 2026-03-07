def calcular_nivel(xp):

    if xp >= 1200:
        return "Divindade do Aço"
    elif xp >= 800:
        return "Titã"
    elif xp >= 500:
        return "Forjador(a)"
    elif xp >= 250:
        return "Guerreiro(a)"
    elif xp >= 100:
        return "Aprendiz"
    else:
        return "Iniciante"