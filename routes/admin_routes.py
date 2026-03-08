from flask import Blueprint, render_template, request, redirect, session
from database.database import conectar

admin_bp = Blueprint("admin", __name__)


# ===============================
# PAINEL ADMIN
# ===============================

@admin_bp.route("/admin")
def admin():

    if "perfil" not in session or session["perfil"] != "admin":
        return redirect("/login")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id,nome,email,perfil
    FROM usuarios
    ORDER BY id DESC
    """)

    usuarios = cursor.fetchall()

    conn.close()

    return render_template(
        "admin.html",
        usuarios=usuarios
    )


# ===============================
# CRIAR USUÁRIO
# ===============================

@admin_bp.route("/criar_usuario", methods=["POST"])
def criar_usuario():

    if "perfil" not in session or session["perfil"] != "admin":
        return redirect("/login")

    nome = request.form["nome"]
    email = request.form["email"]
    senha = request.form["senha"]
    perfil = request.form["perfil"]

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO usuarios
    (nome,email,senha,perfil)
    VALUES (?,?,?,?)
    """,(nome,email,senha,perfil))

    conn.commit()
    conn.close()

    return redirect("/admin")


# ===============================
# EXCLUIR USUÁRIO
# ===============================

@admin_bp.route("/excluir_usuario/<int:id>")
def excluir_usuario(id):

    if "perfil" not in session or session["perfil"] != "admin":
        return redirect("/login")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM usuarios
    WHERE id = ?
    """,(id,))

    conn.commit()
    conn.close()

    return redirect("/admin")