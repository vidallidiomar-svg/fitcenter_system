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

    # total de alunos
    cursor.execute("SELECT COUNT(*) as total FROM alunos")
    resultado = cursor.fetchone()
    total_alunos = resultado["total"] if resultado else 0

    # total de xp
    try:
        cursor.execute("SELECT SUM(xp) as total FROM alunos")
        resultado = cursor.fetchone()
        total_xp = resultado["total"] if resultado["total"] else 0
    except:
        total_xp = 0

    # ranking
    try:
        cursor.execute("""
            SELECT nome, xp
            FROM alunos
            ORDER BY xp DESC
            LIMIT 5
        """)
        ranking = cursor.fetchall()
    except:
        ranking = []

    conn.close()

    return render_template(
        "dashboard.html",
        total_alunos=total_alunos,
        total_xp=total_xp,
        ranking=ranking
    )