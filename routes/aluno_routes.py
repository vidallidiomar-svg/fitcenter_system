from flask import Blueprint, render_template, request, redirect
import os
from database.database import conectar

aluno_bp = Blueprint("aluno", __name__)

UPLOAD_FOLDER = "static/fotos"


@aluno_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    if request.method == "POST":

        nome = request.form["nome"]
        apelido = request.form["apelido"]
        email = request.form["email"]
        senha = request.form["senha"]
        genero = request.form["genero"]

        foto = request.files["foto"]

        nome_foto = None

        if foto:
            nome_foto = foto.filename
            caminho = os.path.join(UPLOAD_FOLDER, nome_foto)
            foto.save(caminho)

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO alunos
        (nome,apelido,email,senha,genero,foto)
        VALUES (?,?,?,?,?,?)
        """, (nome, apelido, email, senha, genero, nome_foto))

        conn.commit()
        conn.close()

        return redirect("/alunos")

    return render_template("cadastro_aluno.html")


@aluno_bp.route("/alunos")
def alunos():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM alunos")

    alunos = cursor.fetchall()

    conn.close()

    return render_template("lista_alunos.html", alunos=alunos)