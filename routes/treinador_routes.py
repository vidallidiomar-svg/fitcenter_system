from flask import Blueprint, render_template, request, redirect
from database.database import conectar
import pandas as pd

treinador_bp = Blueprint("treinador", __name__)


# ===============================
# PAINEL DO TREINADOR
# ===============================

@treinador_bp.route("/treinador")
def painel_treinador():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM alunos")

    alunos = cursor.fetchall()

    conn.close()

    return render_template(
        "treinador.html",
        alunos=alunos
    )


# ===============================
# CRIAR TREINO
# ===============================

@treinador_bp.route("/criar_treino", methods=["POST"])
def criar_treino():

    aluno_id = request.form["aluno_id"]
    nome = request.form["nome"]

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO treinos (aluno_id,nome)

    VALUES (?,?)

    """,(aluno_id,nome))

    conn.commit()
    conn.close()

    return redirect("/treinador")


# ===============================
# ADICIONAR EXERCICIO
# ===============================

@treinador_bp.route("/adicionar_exercicio", methods=["POST"])
def adicionar_exercicio():

    treino_id = request.form["treino_id"]
    ordem = request.form["ordem"]
    nome = request.form["nome"]
    series = request.form["series"]
    repeticoes = request.form["repeticoes"]
    peso = request.form["peso"]
    intervalo = request.form["intervalo"]
    metodo = request.form["metodo"]
    movimento = request.form["movimento"]

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO treino_exercicios
    (treino_id,ordem,nome,series,repeticoes,peso,intervalo,metodo,movimento)

    VALUES (?,?,?,?,?,?,?,?,?)

    """,(treino_id,ordem,nome,series,repeticoes,peso,intervalo,metodo,movimento))

    conn.commit()
    conn.close()

    return redirect("/treinador")


# ===============================
# IMPORTAR TREINO EXCEL
# ===============================

@treinador_bp.route("/importar_treino_excel", methods=["POST"])
def importar_treino_excel():

    arquivo = request.files["arquivo"]

    df = pd.read_excel(arquivo)

    conn = conectar()
    cursor = conn.cursor()

    treino_id = request.form["treino_id"]

    for _, linha in df.iterrows():

        cursor.execute("""

        INSERT INTO treino_exercicios
        (treino_id,ordem,series,repeticoes,peso,intervalo,metodo,movimento)

        VALUES (?,?,?,?,?,?,?,?)

        """, (

        treino_id,
        linha["ordem"],
        linha["series"],
        linha["repeticoes"],
        linha["peso"],
        linha["intervalo"],
        linha["metodo"],
        linha["movimento"]

        ))

    conn.commit()
    conn.close()

    return redirect("/treinador")