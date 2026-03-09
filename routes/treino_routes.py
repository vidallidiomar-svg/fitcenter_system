from flask import Blueprint, render_template, redirect, request
from database.database import conectar
from services.importar_treino_excel import importar_excel
import os

treino_bp = Blueprint("treino", __name__)

UPLOAD_FOLDER = "uploads/treinos"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ===============================
# LISTAR TREINOS DO ALUNO
# ===============================

@treino_bp.route("/treino/<int:aluno_id>")
def treino(aluno_id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM treinos
        WHERE aluno_id = ?
    """, (aluno_id,))

    treinos = cursor.fetchall()

    conn.close()

    return render_template(
        "treino.html",
        treinos=treinos
    )


# ===============================
# VER EXERCÍCIOS DO TREINO
# ===============================

@treino_bp.route("/treino_detalhe/<int:treino_id>")
def treino_detalhe(treino_id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM treino_exercicios
        WHERE treino_id = ?
        ORDER BY ordem
    """, (treino_id,))

    exercicios = cursor.fetchall()

    conn.close()

    return render_template(
        "treino_detalhe.html",
        exercicios=exercicios,
        treino_id=treino_id
    )


# ===============================
# REGISTRAR PESO / OBSERVAÇÃO
# ===============================

@treino_bp.route("/atualizar_exercicio/<int:exercicio_id>", methods=["POST"])
def atualizar_exercicio(exercicio_id):

    peso = request.form.get("peso_aluno")
    observacao = request.form.get("observacao_aluno")
    concluido = request.form.get("concluido")

    if concluido:
        concluido = 1
    else:
        concluido = 0

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE treino_exercicios
        SET peso_aluno = ?,
            observacao_aluno = ?,
            concluido = ?
        WHERE id = ?
    """, (peso, observacao, concluido, exercicio_id))

    conn.commit()
    conn.close()

    return redirect(request.referrer)


# ===============================
# CONCLUIR TREINO
# ===============================

@treino_bp.route("/concluir_treino/<int:treino_id>")
def concluir_treino(treino_id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE treinos
        SET concluido = 1
        WHERE id = ?
    """, (treino_id,))

    conn.commit()
    conn.close()

    return redirect("/")


# ===============================
# UPLOAD DE TREINO
# ===============================

@treino_bp.route("/upload_treino", methods=["POST"])
def upload_treino():

    aluno_id = request.form.get("aluno_id")
    nome = request.form.get("nome")
    arquivo = request.files.get("arquivo")

    if not arquivo:
        return "Arquivo não enviado"

    nome_arquivo = arquivo.filename
    caminho = os.path.join(UPLOAD_FOLDER, nome_arquivo)

    arquivo.save(caminho)

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO treinos
    (aluno_id, nome, arquivo_pdf, concluido)

    VALUES (?,?,?,0)

    """,(aluno_id, nome, nome_arquivo))

    treino_id = cursor.lastrowid

    conn.commit()
    conn.close()

    # se for Excel importar exercícios

    if nome_arquivo.endswith(".xlsx") or nome_arquivo.endswith(".xls"):

        importar_excel(caminho, treino_id)

    return redirect("/treinador")