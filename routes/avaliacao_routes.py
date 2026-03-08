from flask import Blueprint, render_template, request, redirect
from database.database import conectar

avaliacao_bp = Blueprint("avaliacao", __name__)


# ===============================
# AVALIAÇÃO FÍSICA
# ===============================

@avaliacao_bp.route("/avaliacao/<int:aluno_id>", methods=["GET","POST"])
def avaliacao(aluno_id):

    conn = conectar()
    cursor = conn.cursor()

    # SALVAR NOVA AVALIAÇÃO

    if request.method == "POST":

        peso = request.form["peso"]
        gordura = request.form["gordura"]
        massa = request.form["massa"]
        data = request.form["data"]

        cursor.execute("""

        INSERT INTO avaliacoes
        (aluno_id, peso, gordura, massa, data)

        VALUES (?, ?, ?, ?, ?)

        """, (aluno_id, peso, gordura, massa, data))

        conn.commit()

        return redirect(f"/avaliacao/{aluno_id}")

    # BUSCAR HISTÓRICO

    cursor.execute("""

    SELECT peso, gordura, massa, data
    FROM avaliacoes
    WHERE aluno_id = ?
    ORDER BY data DESC

    """, (aluno_id,))

    avaliacoes = cursor.fetchall()

    conn.close()

    return render_template(
        "avaliacao.html",
        avaliacoes=avaliacoes
    )