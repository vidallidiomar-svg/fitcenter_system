from flask import Blueprint, render_template, request, redirect, session
from database.database import conectar
from services.niveis import calcular_nivel
from services.conquistas import verificar_conquistas
from services.streak import calcular_streak

portal_aluno_bp = Blueprint("portal_aluno", __name__)


@portal_aluno_bp.route("/login_aluno", methods=["GET","POST"])
def login_aluno():

    if request.method == "POST":

        email = request.form["email"]
        senha = request.form["senha"]

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM alunos
        WHERE email=? AND senha=?
        """,(email,senha))

        aluno = cursor.fetchone()

        conn.close()

        if aluno:

            session["aluno_id"] = aluno["id"]

            return redirect("/portal")

    return render_template("login_aluno.html")


@portal_aluno_bp.route("/portal")
def portal():

    if "aluno_id" not in session:
        return redirect("/login_aluno")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM alunos WHERE id=?", (session["aluno_id"],))
    aluno = cursor.fetchone()

    cursor.execute("""
    SELECT data
    FROM historico_treino
    WHERE aluno_id=?
    """,(session["aluno_id"],))

    datas = [row["data"] for row in cursor.fetchall()]
    total_treinos = len(datas)

    cursor.execute("""
    SELECT data,peso
    FROM historico_treino
    WHERE aluno_id=?
    ORDER BY data
    """,(session["aluno_id"],))

    historico = cursor.fetchall()

    conn.close()

    datas_grafico = [row["data"] for row in historico]
    pesos_grafico = [row["peso"] for row in historico]

    nivel, xp_base = calcular_nivel(aluno["xp"])
    progresso = int((aluno["xp"] - xp_base) / 100 * 100)

    conquistas = verificar_conquistas(aluno["xp"], total_treinos)
    streak = calcular_streak(datas)

    return render_template(
        "portal_aluno.html",
        aluno=aluno,
        nivel=nivel,
        progresso=progresso,
        conquistas=conquistas,
        streak=streak,
        datas_grafico=datas_grafico,
        pesos_grafico=pesos_grafico
    )