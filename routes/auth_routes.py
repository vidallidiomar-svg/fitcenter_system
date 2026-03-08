from flask import Blueprint, render_template, request, redirect, session
from database.database import conectar

auth_bp = Blueprint("auth", __name__)


# ===============================
# LOGIN
# ===============================

@auth_bp.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        senha = request.form["senha"]

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM usuarios
        WHERE email=? AND senha=?
        """,(email,senha))

        usuario = cursor.fetchone()

        conn.close()

        if usuario:

            session["usuario_id"] = usuario["id"]
            session["perfil"] = usuario["perfil"]

            if usuario["perfil"] == "admin":
                return redirect("/admin")

            if usuario["perfil"] == "treinador":
                return redirect("/treinador")

            if usuario["perfil"] == "nutricionista":
                return redirect("/nutri")

            if usuario["perfil"] == "aluno":
                return redirect("/portal_aluno")

        return render_template("login.html", erro="Login inválido")

    return render_template("login.html")


# ===============================
# LOGOUT
# ===============================

@auth_bp.route("/logout")
def logout():

    session.clear()

    return redirect("/login")