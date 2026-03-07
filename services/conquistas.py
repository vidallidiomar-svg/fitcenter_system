def verificar_conquistas(xp, total_treinos):

    conquistas = []

    if xp >= 100:
        conquistas.append("Primeiro progresso")

    if xp >= 500:
        conquistas.append("Guerreiro do treino")

    if xp >= 1000:
        conquistas.append("Forjador do aço")

    if xp >= 2000:
        conquistas.append("Titã da academia")

    if total_treinos >= 10:
        conquistas.append("10 treinos completos")

    if total_treinos >= 50:
        conquistas.append("50 treinos realizados")

    return conquistas