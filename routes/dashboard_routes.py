from flask import Blueprint, render_template
from database.database import conectar

dashboard_bp = Blueprint("dashboard", __name__)


# ===============================
# DASHBOARD
# ===============================

@dashboard_bp.route("/")
def dashboard():

    conn = conectar()
    cursor = conn.cursor()

    # total de alunos

    cursor.execute("SELECT COUNT(*) as total FROM alunos")
    total = cursor.fetchone()["total"]

    # xp total

    cursor.execute("SELECT SUM(xp) as xp_total FROM alunos")
    resultado = cursor.fetchone()

    xp_total = resultado["xp_total"] if resultado["xp_total"] else 0

    # ranking

    cursor.execute("""
    SELECT nome, xp
    FROM alunos
    ORDER BY xp DESC
    """)

    ranking = cursor.fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        total=total,
        xp_total=xp_total,
        ranking=ranking
    )


# ===============================
# RANKING
# ===============================

@dashboard_bp.route("/ranking")
def ranking():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT nome, xp
    FROM alunos
    ORDER BY xp DESC
    """)

    ranking = cursor.fetchall()

    conn.close()

    return render_template(
        "ranking.html",
        ranking=ranking
    )