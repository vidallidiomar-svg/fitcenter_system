from datetime import datetime


def calcular_streak(datas):

    if not datas:
        return 0

    datas = sorted(datas, reverse=True)

    streak = 1

    for i in range(len(datas)-1):

        d1 = datetime.fromisoformat(datas[i])
        d2 = datetime.fromisoformat(datas[i+1])

        diferenca = (d1 - d2).days

        if diferenca == 1:
            streak += 1
        else:
            break

    return streak