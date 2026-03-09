import pandas as pd
from database.database import conectar


def importar_excel(caminho_excel, treino_id):

    df = pd.read_excel(caminho_excel)

    conn = conectar()
    cursor = conn.cursor()

    ordem = 1

    for _, row in df.iterrows():

        nome = row.get("exercicio")
        series = row.get("series")
        repeticoes = row.get("repeticoes")
        intervalo = row.get("intervalo")
        peso = row.get("peso")
        movimento = row.get("movimento")
        metodo = row.get("metodo")

        cursor.execute("""

        INSERT INTO treino_exercicios
        (
        treino_id,
        ordem,
        nome,
        series,
        repeticoes,
        intervalo,
        peso,
        movimento,
        metodo
        )

        VALUES (?,?,?,?,?,?,?,?,?)

        """,(treino_id,
             ordem,
             nome,
             series,
             repeticoes,
             intervalo,
             peso,
             movimento,
             metodo))

        ordem += 1

    conn.commit()
    conn.close()