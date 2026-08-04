from flask import Blueprint,render_template
from models.tables import Doctor

bp = Blueprint('general', __name__)

@bp.route("/")
def home ():
    return render_template("home.html")



