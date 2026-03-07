from flask import Blueprint, render_template, request, redirect, session
import sqlite3

auth_bp = Blueprint("auth", __name__)


def conectar():

    conn = sqlite3.connect("fitcenter.db")
    conn.row_factory = sqlite3.Row
    return conn


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
            session["tipo"] = usuario["tipo"]

            return redirect("/")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():

    session.clear()

    return redirect("/login")