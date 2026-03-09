from flask import Blueprint, render_template, session, redirect
from database.database import conectar

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
def dashboard():

    # ===============================
    # VERIFICAR LOGIN
    # ===============================

    if "usuario_id" not in session:
        return redirect("/login")

    conn = conectar()
    cursor = conn.cursor()

    # ===============================
    # TOTAL DE ALUNOS
    # ===============================

    cursor.execute("""
    SELECT COUNT(*) as total
    FROM alunos
    """)

    resultado = cursor.fetchone()
    total = resultado["total"] if resultado else 0

    # ===============================
    # XP TOTAL DA ACADEMIA
    # ===============================

    cursor.execute("""
    SELECT SUM(xp) as xp_total
    FROM alunos
    """)

    resultado = cursor.fetchone()

    xp_total = resultado["xp_total"] if resultado and resultado["xp_total"] else 0

    # ===============================
    # RANKING
    # ===============================

    cursor.execute("""
    SELECT nome, xp
    FROM alunos
    ORDER BY xp DESC
    LIMIT 10
    """)

    ranking = cursor.fetchall()

    conn.close()

    # ===============================
    # RENDERIZAR DASHBOARD
    # ===============================

    return render_template(
        "dashboard.html",
        total=total,
        xp_total=xp_total,
        ranking=ranking
    )