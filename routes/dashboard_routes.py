from flask import Blueprint, render_template
from database.database import conectar

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def dashboard():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as total FROM alunos")
    total = cursor.fetchone()["total"]

    cursor.execute("SELECT SUM(xp) as total FROM alunos")
    xp_total = cursor.fetchone()["total"]

    if xp_total is None:
        xp_total = 0

    cursor.execute("SELECT COUNT(*) as total FROM treinos")
    treinos = cursor.fetchone()["total"]

    cursor.execute("""

    SELECT nome,xp
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
        treinos=treinos,
        ranking=ranking
    )