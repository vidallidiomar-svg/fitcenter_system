from flask import Blueprint, render_template, session, redirect

avaliacao_bp = Blueprint("avaliacao", __name__)


@avaliacao_bp.route("/avaliacao")
def avaliacao():

    if "usuario_id" not in session:
        return redirect("/login")

    return render_template("avaliacao.html")