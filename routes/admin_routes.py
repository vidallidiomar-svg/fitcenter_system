from flask import Blueprint, render_template, request, redirect, session
from database.database import conectar

admin_bp = Blueprint("admin", __name__)


# ===============================
# PERMISSÃO ADMIN / SUPORTE
# ===============================

def acesso_admin():

    if "perfil" not in session:
        return False

    if session["perfil"] not in ["admin", "suporte"]:
        return False

    return True


# ===============================
# PAINEL ADMIN
# ===============================

@admin_bp.route("/admin")
def admin():

    if not acesso_admin():
        return redirect("/login")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM usuarios
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

    if not acesso_admin():
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
# EDITAR USUÁRIO
# ===============================

@admin_bp.route("/editar_usuario/<int:id>")
def editar_usuario(id):

    if not acesso_admin():
        return redirect("/login")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM usuarios
    WHERE id=?
    """,(id,))

    usuario = cursor.fetchone()

    conn.close()

    return render_template(
        "editar_usuario.html",
        usuario=usuario
    )


# ===============================
# SALVAR EDIÇÃO
# ===============================

@admin_bp.route("/salvar_usuario/<int:id>", methods=["POST"])
def salvar_usuario(id):

    if not acesso_admin():
        return redirect("/login")

    nome = request.form["nome"]
    email = request.form["email"]
    perfil = request.form["perfil"]

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE usuarios
    SET nome=?, email=?, perfil=?
    WHERE id=?
    """,(nome,email,perfil,id))

    conn.commit()
    conn.close()

    return redirect("/admin")


# ===============================
# EXCLUIR USUÁRIO
# ===============================

@admin_bp.route("/excluir_usuario/<int:id>")
def excluir_usuario(id):

    if not acesso_admin():
        return redirect("/login")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM usuarios
    WHERE id=?
    """,(id,))

    conn.commit()
    conn.close()

    return redirect("/admin")


# ===============================
# RESETAR SENHA
# ===============================

@admin_bp.route("/resetar_senha/<int:id>")
def resetar_senha(id):

    if not acesso_admin():
        return redirect("/login")

    nova_senha = "12345678"

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE usuarios
    SET senha=?
    WHERE id=?
    """,(nova_senha,id))

    conn.commit()
    conn.close()

    return redirect("/admin")