from flask import Blueprint, render_template, request, redirect, session
from database.database import conectar

nutri_bp = Blueprint("nutri", __name__)

@nutri_bp.route("/nutri")
def nutri():

    if "perfil" not in session or session["perfil"] not in ["nutricionista","admin","suporte"]:
        return redirect("/login")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT planos.*, alunos.nome AS aluno_nome
    FROM planos
    JOIN alunos ON planos.aluno_id = alunos.id
    ORDER BY planos.id DESC
    """)

    planos = cursor.fetchall()

    conn.close()

    return render_template(
        "nutri.html",
        planos=planos
    )