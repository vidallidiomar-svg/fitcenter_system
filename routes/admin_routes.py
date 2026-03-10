from flask import Blueprint, render_template, request, redirect, session
from database.database import conectar

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin", methods=["GET","POST"])
def admin():

    if "usuario_id" not in session:
        return redirect("/login")

    if session["perfil"] not in ["admin","suporte"]:
        return redirect("/dashboard")

    conn = conectar()
    cursor = conn.cursor()

    if request.method == "POST":

        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]
        perfil = request.form["perfil"]

        cursor.execute("""
        INSERT INTO usuarios
        (nome,email,senha,perfil)
        VALUES (?,?,?,?)
        """,(nome,email,senha,perfil))

        conn.commit()

    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()

    conn.close()

    return render_template(
        "admin.html",
        usuarios=usuarios
    )


@admin_bp.route("/excluir_usuario/<id>")
def excluir_usuario(id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM usuarios
    WHERE id=?
    """,(id,))

    conn.commit()
    conn.close()

    return redirect("/admin")