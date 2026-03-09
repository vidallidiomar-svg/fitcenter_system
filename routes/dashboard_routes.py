from flask import Blueprint, render_template, session, redirect
from database.database import conectar

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
def dashboard():

    if "usuario_id" not in session:
        return redirect("/login")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as total FROM alunos")
    total = cursor.fetchone()["total"]

    cursor.execute("SELECT SUM(xp) as xp_total FROM alunos")
    xp_total = cursor.fetchone()["xp_total"]

    if xp_total is None:
        xp_total = 0

    cursor.execute("""
    SELECT nome, xp
    FROM alunos
    ORDER BY xp DESC
    LIMIT 10
    """)

    ranking = cursor.fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        total=total,
        xp_total=xp_total,
        ranking=ranking
    )