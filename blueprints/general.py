from flask import Blueprint,render_template
from models.tables import Doctor

bp = Blueprint('general', __name__)

@bp.route("/")
def home ():
    return render_template("home.html")

@bp.route("/taking_turn")
def taking_turn ():
    doctors = Doctor.query.all()
    return render_template("taking_turn.html", doctors=doctors)
