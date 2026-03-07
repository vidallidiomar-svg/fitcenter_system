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

    cursor.execute("SELECT * FROM alunos WHERE id=?", (aluno_id,))
    aluno = cursor.fetchone()

    conn.close()

    return render_template(
        "portal_aluno.html",
        aluno=aluno
    )