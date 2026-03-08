from flask import Blueprint, render_template, request, redirect
from database.database import conectar

exercicios_bp = Blueprint("exercicios", __name__)


# ===============================
# LISTAR EXERCICIOS
# ===============================

@exercicios_bp.route("/exercicios")
def exercicios():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM exercicios")

    exercicios = cursor.fetchall()

    conn.close()

    return render_template(
        "exercicios.html",
        exercicios=exercicios
    )


# ===============================
# CADASTRAR EXERCICIO
# ===============================

@exercicios_bp.route("/novo_exercicio", methods=["POST"])
def novo_exercicio():

    nome = request.form["nome"]
    grupo = request.form["grupo"]
    equipamento = request.form["equipamento"]
    descricao = request.form["descricao"]

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO exercicios
    (nome, grupo, equipamento, descricao)

    VALUES (?,?,?,?)

    """,(nome,grupo,equipamento,descricao))

    conn.commit()
    conn.close()

    return redirect("/exercicios")