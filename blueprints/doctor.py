from flask import Blueprint,render_template,request,flash,redirect,url_for,session
from models.tables import Appointment,Doctor
from werkzeug.security import check_password_hash

bp = Blueprint("doctor", __name__, url_prefix="/doctor")

@bp.route("/dashboard/<int:id>")
def dashboard (id):

    appointment = Appointment.query.filter_by(doctor_id=id).all()
    return render_template("doctor/doctor_dashboard.html", appointment=appointment)


@bp.route("/login", methods=["GET", "POST"])
def doctor_login():

    if request.method == "GET":
        return render_template("doctor/doctor_login.html", id=id)

    phone = request.form.get("phone").strip()
    password = request.form.get("password").strip()

    doctor = Doctor.query.filter_by(phone=phone).first()

    if doctor is None or not check_password_hash(doctor.password, password):
        flash("شماره موبایل یا رمز اشتباه است", "error")
        return redirect(url_for("doctor.doctor_login"))

    session["doctor_id"] = doctor.id

    flash("با موفقیت وارد شدید", "success")
    return redirect(url_for("doctor.dashboard", id=doctor.id))

