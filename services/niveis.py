def calcular_nivel(xp):

    if xp >= 5000:
        return "Divindade do aço", 5000

    elif xp >= 2000:
        return "Titã", 2000

    elif xp >= 1000:
        return "Forjador(a)", 1000

    elif xp >= 500:
        return "Guerreiro(a)", 500

    elif xp >= 200:
        return "Aprendiz", 200

    else:
        return "Iniciante", 0