from flask import Blueprint, render_template, session, redirect
from database.database import conectar

aluno_portal_bp = Blueprint("aluno_portal", __name__)


@aluno_portal_bp.route("/portal_aluno")
def portal_aluno():

    if "aluno_id" not in session:
        return redirect("/login")

    aluno_id = session["aluno_id"]

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM alunos WHERE id=?",
        (aluno_id,)
    )

    aluno = cursor.fetchone()

    cursor.execute("""
        SELECT *
        FROM avaliacoes
        WHERE aluno_id = ?
        ORDER BY id
    """,(aluno_id,))

    dados = cursor.fetchall()

    datas_grafico = []
    pesos_grafico = []

    for d in dados:

        datas_grafico.append(d["data"])
        pesos_grafico.append(d["peso"])

    xp = aluno["xp"]

    nivel = xp // 100
    progresso = xp % 100

    streak = aluno["streak"]

    conn.close()

    return render_template(
        "portal_aluno.html",
        aluno=aluno,
        progresso=progresso,
        nivel=nivel,
        streak=streak,
        datas_grafico=datas_grafico,
        pesos_grafico=pesos_grafico
    )