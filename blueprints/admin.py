from flask import Blueprint,render_template,request,session,abort,flash,redirect,url_for
from config import ADMIN_USERNAME,ADMIN_PASSWORD
from models.tables import Doctor
from extentions import db
from werkzeug.utils import secure_filename
import os


bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.before_request
def before_request() :
    if session.get("admin_login") is None and request.endpoint != "admin.login" :
        abort(403)

#====================
# ADMIN Login
#====================
@bp.route("/login", methods=['GET', 'POST'])
def login() :
    if request.method == "GET" :
        return render_template("admin/admin_login.html")
    
    username = request.form['username']
    password = request.form['password']

    if username != ADMIN_USERNAME or password != ADMIN_PASSWORD :
        flash("رمز عبور یا نام کاربری اشتباه است", "error")
        return redirect(url_for("admin.login"))

    session["admin_login"] = username
    flash("با موفقیت وارد شدید", "success")
    return redirect(url_for("admin.dashboard"))


#====================
# ADMIN Logout
#====================
@bp.route("/logout")
def logout():
    session.pop("admin_login", None)  # حذف لاگین ادمین
    flash("با موفقیت از پنل مدیریت خارج شدید", "success")
    return redirect(url_for("admin.login"))


#====================
# ADMIN Dashboard
#====================
@bp.route("/dashboard", methods=['GET', 'POST'])
def dashboard ():
    if request.method == "POST":

        doctor_name = request.form.get("doctor_name").strip()
        experience_years = request.form.get("experience_years").strip()
        biography = request.form.get("biography").strip()
        visit_price = request.form.get("visit_price").strip()
        specials = request.form.get("specials").strip()

        profile_image = request.files.get("profile_image")

        doctor = Doctor(
            doctor_name=doctor_name,
            experience_years=experience_years,
            biography=biography,
            visit_price=visit_price,
            specials=specials
        )

        db.session.add(doctor)
        db.session.commit()

        if profile_image and profile_image.filename != "":

            filename = secure_filename(profile_image.filename)

            profile_image.save(os.path.join("static", "doctor_profile", filename))

            doctor.profile_image = filename

            db.session.commit()

        flash("دکتر با موفقیت ثبت شد.", "success")

        return redirect(url_for("admin.dashboard"))

    return render_template("admin/admin_dashboard.html")

    


