from flask import Blueprint, render_template, request, redirect
from database.database import conectar
from werkzeug.utils import secure_filename
import os
import pandas as pd

treinador_bp = Blueprint("treinador", __name__)

UPLOAD_FOLDER = "uploads/treinos"

# garante que a pasta exista
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ===============================
# DASHBOARD TREINADOR
# ===============================

@treinador_bp.route("/treinador")
def treinador():

    conn = conectar()
    cursor = conn.cursor()

    # total alunos
    cursor.execute("SELECT COUNT(*) as total FROM alunos")
    total_alunos = cursor.fetchone()["total"]

    # xp total
    cursor.execute("SELECT SUM(xp) as xp_total FROM alunos")
    xp_total = cursor.fetchone()["xp_total"]

    if xp_total is None:
        xp_total = 0

    # exercícios concluídos
    cursor.execute("""
    SELECT COUNT(*) as total
    FROM treino_exercicios
    WHERE concluido = 1
    """)

    exercicios_concluidos = cursor.fetchone()["total"]

    # ranking
    cursor.execute("""
    SELECT nome, xp
    FROM alunos
    ORDER BY xp DESC
    LIMIT 5
    """)

    ranking = cursor.fetchall()

    conn.close()

    return render_template(
        "treinador.html",
        total_alunos=total_alunos,
        xp_total=xp_total,
        exercicios_concluidos=exercicios_concluidos,
        ranking=ranking
    )


# ===============================
# UPLOAD TREINO PDF
# ===============================

@treinador_bp.route("/upload_treino", methods=["POST"])
def upload_treino():

    aluno_id = request.form["aluno_id"]
    nome = request.form["nome"]

    arquivo = request.files["arquivo"]

    if arquivo and arquivo.filename != "":

        nome_arquivo = secure_filename(arquivo.filename)

        caminho = os.path.join(UPLOAD_FOLDER, nome_arquivo)

        arquivo.save(caminho)

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""

        INSERT INTO treinos
        (aluno_id, nome, arquivo_pdf)

        VALUES (?, ?, ?)

        """,(aluno_id, nome, nome_arquivo))

        conn.commit()
        conn.close()

    return redirect("/treinador")
# ===============================
# IMPORTAR TREINO EXCEL
# ===============================

@treinador_bp.route("/importar_treino_excel", methods=["POST"])
def importar_treino_excel():

    aluno_id = request.form["aluno_id"]

    arquivo = request.files["arquivo"]

    df = pd.read_excel(arquivo)

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO treinos
    (aluno_id,nome)

    VALUES (?,?)

    """,(aluno_id,"Treino Excel"))

    treino_id = cursor.lastrowid

    for index,row in df.iterrows():

        cursor.execute("""

        INSERT INTO treino_exercicios
        (treino_id,nome,series,repeticoes,peso)

        VALUES (?,?,?,?,?)

        """,(treino_id,row["exercicio"],row["series"],row["reps"],row["peso"]))

    conn.commit()
    conn.close()

    return redirect("/treinador")