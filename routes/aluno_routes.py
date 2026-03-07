from flask import Blueprint, render_template, request, redirect, send_file
from database.database import conectar

import pandas as pd
from reportlab.pdfgen import canvas

aluno_bp = Blueprint("aluno", __name__)


# ===============================
# LISTAR ALUNOS
# ===============================

@aluno_bp.route("/alunos")
def alunos():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM alunos")

    alunos = cursor.fetchall()

    conn.close()

    return render_template(
        "lista_alunos.html",
        alunos=alunos
    )


# ===============================
# CADASTRAR ALUNO
# ===============================

@aluno_bp.route("/cadastro", methods=["GET","POST"])
def cadastro():

    if request.method == "POST":

        nome = request.form["nome"]
        apelido = request.form["apelido"]
        email = request.form["email"]
        senha = request.form["senha"]
        genero = request.form["genero"]

        # VALIDAÇÃO DE SENHA

        if len(senha) < 8:

            return render_template(
                "cadastro_aluno.html",
                erro="A senha deve ter no mínimo 8 caracteres"
            )

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""

        INSERT INTO alunos
        (nome, apelido, email, senha, genero, xp, streak)

        VALUES (?, ?, ?, ?, ?, ?, ?)

        """, (nome, apelido, email, senha, genero, 0, 0))

        conn.commit()
        conn.close()

        return redirect("/alunos")

    return render_template("cadastro_aluno.html")


# ===============================
# EXPORTAR ALUNOS PARA EXCEL
# ===============================

@aluno_bp.route("/exportar_excel")
def exportar_excel():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""

    SELECT nome, apelido, email, xp, streak
    FROM alunos

    """)

    dados = cursor.fetchall()

    conn.close()

    df = pd.DataFrame(dados)

    arquivo = "alunos.xlsx"

    df.to_excel(arquivo, index=False)

    return send_file(
        arquivo,
        as_attachment=True
    )


# ===============================
# GERAR PDF DO ALUNO
# ===============================

@aluno_bp.route("/aluno_pdf/<int:aluno_id>")
def aluno_pdf(aluno_id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""

    SELECT nome, apelido, email, xp, streak
    FROM alunos
    WHERE id = ?

    """, (aluno_id,))

    aluno = cursor.fetchone()

    conn.close()

    arquivo = f"aluno_{aluno_id}.pdf"

    c = canvas.Canvas(arquivo)

    c.setFont("Helvetica", 14)

    c.drawString(100, 800, "FICHA DO ALUNO")

    c.drawString(100, 760, f"Nome: {aluno['nome']}")
    c.drawString(100, 730, f"Apelido: {aluno['apelido']}")
    c.drawString(100, 700, f"Email: {aluno['email']}")
    c.drawString(100, 670, f"XP: {aluno['xp']}")
    c.drawString(100, 640, f"Streak: {aluno['streak']}")

    c.save()

    return send_file(
        arquivo,
        as_attachment=True
    )