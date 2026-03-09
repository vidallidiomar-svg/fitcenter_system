from flask import Blueprint, render_template, redirect
from database.database import conectar
import pandas as pd

treino_bp = Blueprint("treino", __name__)


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