from flask import Blueprint, render_template, request, redirect, session
from database.database import conectar

nutri_bp = Blueprint("nutri", __name__)


# ===============================
# PAINEL DO NUTRICIONISTA
# ===============================

@nutri_bp.route("/nutri")
def nutri():

    if "perfil" not in session or session["perfil"] not in ["nutricionista","admin"]:
        return redirect("/login")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT planos.*, alunos.nome AS aluno_nome
    FROM planos
    JOIN alunos ON planos.aluno_id = alunos.id
    ORDER BY planos.id DESC
    """)

    planos = cursor.fetchall()

    conn.close()

    return render_template(
        "nutri.html",
        planos=planos
    )


# ===============================
# CRIAR PLANO ALIMENTAR
# ===============================

@nutri_bp.route("/criar_plano", methods=["POST"])
def criar_plano():

    if "perfil" not in session or session["perfil"] not in ["nutricionista","admin"]:
        return redirect("/login")

    aluno_id = request.form["aluno_id"]
    nome = request.form["nome"]

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO planos
    (aluno_id, nome)

    VALUES (?,?)

    """,(aluno_id, nome))

    conn.commit()
    conn.close()

    return redirect("/nutri")


# ===============================
# VISUALIZAR PLANO
# ===============================

@nutri_bp.route("/plano/<int:plano_id>")
def plano(plano_id):

    if "perfil" not in session or session["perfil"] not in ["nutricionista","admin"]:
        return redirect("/login")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""

    SELECT *
    FROM refeicoes
    WHERE plano_id = ?

    """,(plano_id,))

    refeicoes = cursor.fetchall()

    cursor.execute("""

    SELECT 
    SUM(calorias) AS calorias,
    SUM(proteina) AS proteina,
    SUM(carbo) AS carbo,
    SUM(gordura) AS gordura
    FROM refeicoes
    WHERE plano_id = ?

    """,(plano_id,))

    macros = cursor.fetchone()

    conn.close()

    return render_template(
        "plano.html",
        plano_id=plano_id,
        refeicoes=refeicoes,
        macros=macros
    )


# ===============================
# ADICIONAR REFEIÇÃO
# ===============================

@nutri_bp.route("/adicionar_refeicao", methods=["POST"])
def adicionar_refeicao():

    if "perfil" not in session or session["perfil"] not in ["nutricionista","admin"]:
        return redirect("/login")

    plano_id = request.form["plano_id"]
    refeicao = request.form["refeicao"]
    alimento = request.form["alimento"]
    quantidade = request.form["quantidade"]

    calorias = request.form["calorias"]
    proteina = request.form["proteina"]
    carbo = request.form["carbo"]
    gordura = request.form["gordura"]

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO refeicoes
    (plano_id, refeicao, alimento, quantidade, calorias, proteina, carbo, gordura)

    VALUES (?,?,?,?,?,?,?,?)

    """,(plano_id, refeicao, alimento, quantidade, calorias, proteina, carbo, gordura))

    conn.commit()
    conn.close()

    return redirect(f"/plano/{plano_id}")


# ===============================
# EXCLUIR REFEIÇÃO
# ===============================

@nutri_bp.route("/excluir_refeicao/<int:id>/<int:plano_id>")
def excluir_refeicao(id, plano_id):

    if "perfil" not in session or session["perfil"] not in ["nutricionista","admin"]:
        return redirect("/login")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM refeicoes
    WHERE id = ?
    """,(id,))

    conn.commit()
    conn.close()

    return redirect(f"/plano/{plano_id}")