from flask import Blueprint, render_template, request, redirect, session

from database.database import conectar

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        senha = request.form["senha"]

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""

        SELECT * FROM usuarios
        WHERE email = ? AND senha = ?

        """,(email,senha))

        usuario = cursor.fetchone()

        conn.close()

        if usuario:

            session["usuario"] = usuario["id"]
            session["tipo"] = usuario["tipo"]

            if usuario["tipo"] == "admin":

                return redirect("/")

            if usuario["tipo"] == "treinador":

                return redirect("/treinador")

            if usuario["tipo"] == "nutricionista":

                return redirect("/nutri")

            if usuario["tipo"] == "aluno":

                return redirect("/portal")

        return "Login inválido"

    return render_template("login.html")