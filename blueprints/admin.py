from flask import Blueprint,render_template,request,session,abort,flash,redirect,url_for
from config import ADMIN_USERNAME,ADMIN_PASSWORD
from models.tables import Doctor,DoctorSchedule
from extentions import db
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from werkzeug.security import generate_password_hash


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
    if request.method == "GET" :
        doctors = Doctor.query.all()
        return render_template("admin/admin_dashboard.html", doctors=doctors)
    

    doctor_name = request.form.get("doctor_name", "").strip()
    experience_years = int(request.form.get("experience_years") or 0) 
    biography = request.form.get("biography", "").strip()
    visit_price = int(request.form.get("visit_price") or 0)
    specials = request.form.get("specials", "").strip()
    phone = request.form.get("phone", "").strip()
    password = generate_password_hash(request.form.get("password", "").strip())

    profile_image = request.files.get("profile_image", "")


    doctor = Doctor(
        doctor_name=doctor_name,
        experience_years=experience_years,
        biography=biography,
        visit_price=visit_price,
        specials=specials,
        phone=phone,
        password=password
    )

    db.session.add(doctor)
    db.session.commit()

    if profile_image and profile_image.filename != "":

        filename = secure_filename(profile_image.filename)

        profile_image.save(os.path.join("static", "doctor_profile", filename))

        doctor.profile_image = filename # چون یدونه عکس هستش و همچنین نام فایل رو میذاره توی جدول دیتابیس

        db.session.commit()

    flash("دکتر با موفقیت ثبت شد.", "success")

    return redirect(url_for("admin.dashboard"))


#====================
# ADMIN Edit Doctor
#====================
@bp.route("/doctor/edit/<int:id>", methods=["GET", "POST"])
def edit_doctor(id):

    doctor = Doctor.query.get_or_404(id)

    if request.method == "POST":

        doctor.doctor_name = request.form.get("doctor_name").strip()
        doctor.experience_years = int(request.form.get("experience_years"))
        doctor.biography = request.form.get("biography").strip()
        doctor.visit_price = int(request.form.get("visit_price"))
        doctor.specials = request.form.get("specials").strip()
        doctor.template_name = request.form.get("template_name").strip()

        profile_image = request.files.get("profile_image")


        if profile_image and profile_image.filename != "":

            # حذف عکس قبلی
            if doctor.profile_image:
            
                old_image = os.path.join("static", "doctor_profile", doctor.profile_image)
                if os.path.exists(old_image): os.remove(old_image)

            # ایجاد عکس جدید
            filename = secure_filename(profile_image.filename)

            profile_image.save(os.path.join("static", "doctor_profile", filename))

            doctor.profile_image = filename

        db.session.commit()

        flash("اطلاعات دکتر با موفقیت ویرایش شد.", "success")

        return redirect(url_for("admin.dashboard"))

    return render_template("admin/edit_doctor.html", doctor=doctor)






#====================
# ADMIN Delete Doctor Image
#====================
@bp.route("/dashboard/delete/<int:id>", methods=["POST"])
def delete_doctor(id):

    # حذف اطلاعات دکتر
    doctor = Doctor.query.get_or_404(id)

    # حذف خود عکس دکتر
    if doctor.profile_image:

        image_path = os.path.join("static", "doctor_profile", doctor.profile_image)
        
        if os.path.exists(image_path): os.remove(image_path)

    db.session.delete(doctor)
    db.session.commit()

    flash("دکتر با موفقیت حذف شد.", "success")

    return redirect(url_for("admin.dashboard"))




#====================
# ADMIN Doctor Schedule
#====================

@bp.route("/add_schedule", methods=["GET","POST"])
def add_schedule():

    if not session.get("admin_login"):
            abort(403)

    if request.method == "GET" :
        doctors = Doctor.query.all()
        return render_template("admin/doctor_schedule.html", doctors=doctors)



    doctor_id = request.form.get("doctor_id")
    day_of_week = request.form.get("day_of_week")
    start_time = request.form.get("start_time")
    end_time = request.form.get("end_time")
    max_visits = int(request.form.get("max_visits" ))


    # checkbox
    active = "active" in request.form


    # بررسی وجود پزشک
    doctor = Doctor.query.get(doctor_id)

    if not doctor:
        flash("دکتر مورد نظر پیدا نشد", "error")
        return redirect(url_for("admin.dashboard"))


    if not start_time or not end_time:
        flash("ساعت شروع و پایان الزامی است", "error")
        return redirect(url_for("admin.dashboard"))


    # تبدیل ساعت به Time
    start_time = datetime.strptime(
        start_time,
        "%H:%M" # H => hours   and   M => minute
    ).time() 


    end_time = datetime.strptime(
        end_time,
        "%H:%M"
    ).time()


    # ساخت برنامه کاری در دیتابیس
    schedule = DoctorSchedule(
        doctor_id=doctor.id,
        day_of_week=day_of_week,
        start_time=start_time,
        end_time=end_time,
        active=active,
        max_visits=max_visits
    )

    db.session.add(schedule)
    db.session.commit()


    flash("برنامه کاری پزشک با موفقیت ثبت شد", "success")
    return redirect(url_for("admin.add_schedule"))





#===========================
# ADMIN Edit Doctor Schedule
#===========================
@bp.route("/edit_add_schedule/<int:id>", methods=["GET","POST"])
def edit_want_doctor(id):

    if not session.get("admin_login"):
        abort(403)

    if request.method == "GET" :
        doctor = Doctor.query.get_or_404(id)
        return render_template("admin/edit_add_schedule.html", doctor=doctor)




#====================================================
# ADMIN Edit Doctor Schedule JUST Button Edit Click
#====================================================
@bp.route("/edit_doctor_schedule/<int:id>", methods=["POST"])
def edit_doctor_schedule(id):

    if not session.get("admin_login"):
        abort(403)

    schedule = DoctorSchedule.query.get_or_404(id)

    schedule.day_of_week = request.form.get("day_of_week")

    schedule.start_time = datetime.strptime(
        request.form.get("start_time"),
        "%H:%M"
    ).time()

    schedule.end_time = datetime.strptime(
        request.form.get("end_time"),
        "%H:%M"
    ).time()

    schedule.max_visits = int(request.form.get("max_visits"))

    schedule.active = "active" in request.form

    db.session.commit()

    flash("برنامه کاری با موفقیت ویرایش شد.", "success")

    return redirect(url_for("admin.edit_want_doctor",id=schedule.doctor_id))





#==============================
# ADMIN Delete Doctor Schedule
#==============================
@bp.route("/delete_doctor_schedule/<int:id>", methods=["POST"])
def delete_doctor_schedule(id):

    if not session.get("admin_login"):
        abort(403)

    doctor_schedule = DoctorSchedule.query.get_or_404(id)

    doctor_id = doctor_schedule.doctor_id # برای اینکه روت بتواند همین صفحه را بشناسد

    db.session.delete(doctor_schedule)
    db.session.commit()

    flash("برنامه کاری دکتر با موفقیت حذف شد", "success")
    return redirect(url_for("admin.edit_want_doctor", id=doctor_id))
    



#=========================================
# ADMIN Doctor Change PHONE and PASSWORD
#=========================================

@bp.route("/doctor_important", methods=["GET", "POST"])
def doctor_important ():
    if request.method == "GET" :
        doctors = Doctor.query.all()
        return render_template("admin/admin_doctor_important.html", doctors=doctors)

    return redirect(url_for("admin.doctor_important"))
    



    
