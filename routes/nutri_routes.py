from flask import Blueprint, render_template
from database.database import conectar

treinador_bp = Blueprint("treinador", __name__)


# ===============================
# DASHBOARD TREINADOR
# ===============================

@treinador_bp.route("/treinador")
def treinador():

    conn = conectar()
    cursor = conn.cursor()

    # total alunos
    cursor.execute("SELECT COUNT(*) as total FROM alunos")
    total_alunos = cursor.fetchone()["total"]

    # xp total academia
    cursor.execute("SELECT SUM(xp) as xp_total FROM alunos")
    xp_total = cursor.fetchone()["xp_total"]

    if xp_total is None:
        xp_total = 0

    # exercícios concluídos
    cursor.execute("""

    SELECT COUNT(*) as total
    FROM treino_exercicios
    WHERE concluido = 1

    """)

    exercicios_concluidos = cursor.fetchone()["total"]

    # ranking alunos
    cursor.execute("""

    SELECT nome, xp
    FROM alunos
    ORDER BY xp DESC
    LIMIT 5

    """)

    ranking = cursor.fetchall()

    conn.close()

    return render_template(
        "treinador.html",
        total_alunos=total_alunos,
        xp_total=xp_total,
        exercicios_concluidos=exercicios_concluidos,
        ranking=ranking
    )


# ===============================
# PROGRESSO DO ALUNO
# ===============================

@treinador_bp.route("/progresso_aluno/<int:aluno_id>")
def progresso_aluno(aluno_id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""

    SELECT nome
    FROM alunos
    WHERE id = ?

    """,(aluno_id,))

    aluno = cursor.fetchone()

    cursor.execute("""

    SELECT nome, peso_real, reps_real
    FROM treino_exercicios
    WHERE treino_id IN
    (SELECT id FROM treinos WHERE aluno_id = ?)
    AND concluido = 1

    """,(aluno_id,))

    progresso = cursor.fetchall()

    conn.close()

    return render_template(
        "progresso_aluno.html",
        aluno=aluno,
        progresso=progresso
    )