from flask import Blueprint,render_template
from models.tables import Doctor

bp = Blueprint('general', __name__)

@bp.route("/")
def home ():
    doctor = Doctor.query.all()
    return render_template("home.html", doctor=doctor)



@bp.route("/general/about")
def about ():
    return render_template("about.html")

@bp.route("/general/bakhsh_ha")
def bakhsh_ha ():
    return render_template("bakhsh_ha.html")

@bp.route("/general/clinic_ha")
def clinic_ha ():
    return render_template("clinic_ha.html")

@bp.route("/general/akhbar")
def akhbar ():
    return render_template("akhbar.html")

@bp.route("/general/gallery")
def gallery ():
    return render_template("gallery.html")

@bp.route("/general/ertebat_ba_ma")
def ertebat_ba_ma ():
    return render_template("ertebat_ba_ma.html")