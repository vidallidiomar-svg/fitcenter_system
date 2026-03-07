from flask import Blueprint, render_template, request, redirect
import sqlite3

treino_bp = Blueprint("treino", __name__)


def conectar():
    conn = sqlite3.connect("fitcenter.db")
    conn.row_factory = sqlite3.Row
    return conn


@treino_bp.route("/treino/<int:aluno_id>")
def treino(aluno_id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM exercicios
    WHERE aluno_id=?
    """,(aluno_id,))

    exercicios = cursor.fetchall()

    conn.close()

    return render_template(
        "treino.html",
        exercicios=exercicios,
        aluno_id=aluno_id
    )


@treino_bp.route("/criar_exercicio/<int:aluno_id>", methods=["POST"])
def criar_exercicio(aluno_id):

    nome = request.form["nome"]
    series = request.form["series"]
    repeticoes = request.form["repeticoes"]
    peso = request.form["peso"]

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO exercicios
    (aluno_id,nome,series,repeticoes,peso)
    VALUES (?,?,?,?,?)
    """,(aluno_id,nome,series,repeticoes,peso))

    conn.commit()
    conn.close()

    return redirect(f"/treino/{aluno_id}")