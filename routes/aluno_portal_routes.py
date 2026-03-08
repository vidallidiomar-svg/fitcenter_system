from flask import Blueprint, render_template, session
from database.database import conectar

aluno_portal_bp = Blueprint("aluno_portal", __name__)


# ===============================
# PORTAL DO ALUNO
# ===============================

@aluno_portal_bp.route("/portal_aluno")
def portal_aluno():

    if "aluno_id" not in session:
        return "Aluno não logado"

    aluno_id = session["aluno_id"]

    conn = conectar()
    cursor = conn.cursor()

    # ===============================
    # DADOS DO ALUNO
    # ===============================

    cursor.execute(
        "SELECT * FROM alunos WHERE id=?",
        (aluno_id,)
    )

    aluno = cursor.fetchone()

    # ===============================
    # AVALIAÇÕES (para gráfico)
    # ===============================

    cursor.execute("""

    SELECT data, peso
    FROM avaliacoes
    WHERE aluno_id = ?
    ORDER BY data

    """,(aluno_id,))

    dados = cursor.fetchall()

    datas_grafico = []
    pesos_grafico = []

    for d in dados:

        datas_grafico.append(d["data"])
        pesos_grafico.append(d["peso"])

    # ===============================
    # XP / NÍVEL
    # ===============================

    xp = aluno["xp"]

    nivel = xp // 100
    progresso = xp % 100

    # ===============================
    # STREAK
    # ===============================

    streak = aluno["streak"] if "streak" in aluno.keys() else 0

    # ===============================
    # CONQUISTAS
    # ===============================

    conquistas = []

    if xp >= 100:
        conquistas.append("Primeiro nível alcançado")

    if xp >= 500:
        conquistas.append("Atleta dedicado")

    if xp >= 1000:
        conquistas.append("Monstro da academia")

    conn.close()

    return render_template(
        "portal_aluno.html",
        aluno=aluno,
        progresso=progresso,
        nivel=nivel,
        streak=streak,
        conquistas=conquistas,
        datas_grafico=datas_grafico,
        pesos_grafico=pesos_grafico
    )