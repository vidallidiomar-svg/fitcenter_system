from flask import Blueprint, render_template, session, redirect
import sqlite3

dashboard_bp = Blueprint("dashboard", __name__)


def conectar():

    conn = sqlite3.connect("fitcenter.db")
    conn.row_factory = sqlite3.Row
    return conn


@dashboard_bp.route("/")
def dashboard():

    if "usuario_id" not in session:
        return redirect("/login")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as total FROM alunos")
    total_alunos = cursor.fetchone()["total"]

    cursor.execute("SELECT SUM(xp) as total FROM alunos")
    xp_total = cursor.fetchone()["total"] or 0

    cursor.execute("SELECT COUNT(*) as total FROM historico_treino")
    total_treinos = cursor.fetchone()["total"]

    cursor.execute("""
    SELECT nome,xp
    FROM alunos
    ORDER BY xp DESC
    LIMIT 5
    """)

    ranking = cursor.fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        total_alunos=total_alunos,
        xp_total=xp_total,
        total_treinos=total_treinos,
        ranking=ranking
    )