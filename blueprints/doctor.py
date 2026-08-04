from flask import Blueprint,render_template,request,flash,redirect,url_for
from models.tables import Appointment,Doctor
from werkzeug.security import generate_password_hash

bp = Blueprint("doctor", __name__, url_prefix="/doctor")

@bp.route("/dashboard")
def dashboard ():


    appointment = Appointment.query.all()
    return render_template("doctor/doctor_dashboard.html", appointment=appointment)


@bp.route("/login", methods=["GET" ,"POST"])
def doctor_login():

    if request.method == "GET" :
        return render_template("doctor/doctor_login.html")

    phone = request.form.get("phone").strip()
    password = request.form.get("password").strip()


    doctor = Doctor.query.filter_by(
        phone=phone,
        password=generate_password_hash(password)
    )

    if doctor is None :
        flash("شماره موبایل یا رمز اشتباه است", "error")
        return redirect(url_for("doctor.doctor_login"))
    
    return redirect (url_for("doctor.dashboard"))

