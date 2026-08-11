from flask import Blueprint,render_template,request
from sqlalchemy import or_
from models.tables import Doctor

bp = Blueprint('general', __name__)

@bp.route("/")
def home ():
    doctor = Doctor.query.all()
    return render_template("home.html", doctor=doctor)

#=======================
# SEARCH Doctor
#=======================
@bp.route("/search")
def search():

    search = request.args.get("search", "").strip()

    doctors = Doctor.query.filter(
        or_(
            Doctor.doctor_name.ilike(f"%{search}%"),
            Doctor.specials.ilike(f"%{search}%")
        )
    ).all()

    return render_template("search.html", doctors=doctors, search=search)




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