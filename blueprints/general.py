from flask import Blueprint,render_template

bp = Blueprint('general', __name__)

@bp.route("/")
def home ():
    return render_template("home.html")

@bp.route("/taking_turn")
def taking_turn ():
    return render_template("taking_turn.html")
