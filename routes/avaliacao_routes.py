from flask import Blueprint, render_template, request, redirect, session
from database.database import conectar

avaliacao_bp = Blueprint("avaliacao", __name__)


@avaliacao_bp.route("/avaliacao", methods=["GET","POST"])
def avaliacao():

    if "usuario_id" not in session:
        return redirect("/login")

    conn = conectar()
    cursor = conn.cursor()

    if request.method == "POST":

        peso = request.form["peso"]
        gordura = request.form["gordura"]
        massa = request.form["massa"]
        data = request.form["data"]

        cursor.execute("""
        INSERT INTO avaliacoes
        (peso,gordura,massa,data)
        VALUES (?,?,?,?)
        """,(peso,gordura,massa,data))

        conn.commit()

    cursor.execute("""
    SELECT peso,gordura,massa,data
    FROM avaliacoes
    ORDER BY data DESC
    """)

    avaliacoes = cursor.fetchall()

    conn.close()

    return render_template(
        "avaliacao.html",
        avaliacoes=avaliacoes
    )