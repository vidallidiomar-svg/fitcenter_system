from flask import Blueprint, render_template, redirect, request
from database.database import conectar
import os

treino_bp = Blueprint("treino", __name__)

UPLOAD_FOLDER = "uploads/treinos"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ===============================
# VER TREINOS DO ALUNO
# ===============================

@treino_bp.route("/treino/<int:aluno_id>")
def treino(aluno_id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM treinos
        WHERE aluno_id = ?
    """,(aluno_id,))

    treinos = cursor.fetchall()

    conn.close()

    return render_template(
        "treino.html",
        treinos=treinos
    )


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
    """,(treino_id,))

    conn.commit()
    conn.close()

    return redirect("/")


# ===============================
# UPLOAD DE TREINO (PDF ou Excel)
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
        (aluno_id, nome, arquivo, concluido)
        VALUES (?, ?, ?, 0)
    """,(aluno_id, nome, nome_arquivo))

    conn.commit()
    conn.close()

    return redirect("/treinador")