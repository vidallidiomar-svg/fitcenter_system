def calcular_nivel(xp, genero):

    if xp < 100:
        return "Iniciante"

    elif xp < 250:
        return "Aprendiz"

    elif xp < 500:
        return "Guerreiro" if genero == "M" else "Guerreira"

    elif xp < 800:
        return "Forjador" if genero == "M" else "Forjadora"

    elif xp < 1200:
        return "Titã"

    else:
        return "Divindade do Aço"