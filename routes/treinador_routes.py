from flask import Blueprint, render_template, request, redirect
from database.database import conectar
import os

treinador_bp = Blueprint("treinador", __name__)

UPLOAD_FOLDER = "uploads/treinos"


# ===============================
# DASHBOARD TREINADOR
# ===============================

@treinador_bp.route("/treinador")
def treinador():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as total FROM alunos")
    total_alunos = cursor.fetchone()["total"]

    cursor.execute("SELECT SUM(xp) as xp_total FROM alunos")
    xp_total = cursor.fetchone()["xp_total"]

    if xp_total is None:
        xp_total = 0

    cursor.execute("""
    SELECT COUNT(*) as total
    FROM treino_exercicios
    WHERE concluido = 1
    """)

    exercicios_concluidos = cursor.fetchone()["total"]

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
# UPLOAD TREINO PDF
# ===============================

@treinador_bp.route("/upload_treino", methods=["POST"])
def upload_treino():

    aluno_id = request.form["aluno_id"]
    nome = request.form["nome"]

    arquivo = request.files["arquivo"]

    if arquivo:

        caminho = os.path.join(UPLOAD_FOLDER, arquivo.filename)

        arquivo.save(caminho)

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""

        INSERT INTO treinos
        (aluno_id, nome, arquivo_pdf)

        VALUES (?, ?, ?)

        """,(aluno_id, nome, arquivo.filename))

        conn.commit()
        conn.close()

    return redirect("/treinador")