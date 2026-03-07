from flask import Blueprint, render_template

nutri_bp = Blueprint("nutri", __name__)


@nutri_bp.route("/nutri")
def nutri():

    return render_template("nutri.html")