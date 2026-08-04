from flask import Blueprint,render_template,request,redirect,flash,url_for
from models.tables import User,Doctor,DoctorSchedule,Appointment
from extentions import db
from flask_login import login_user, login_required,current_user,logout_user
import re
from flask import session
import random
from datetime import datetime, timedelta



bp = Blueprint("user", __name__, url_prefix="/user")

#===================
# USER Dashboard
#===================
@login_required
@bp.route("/dashboard", methods=["GET"])
def dashboard ():
    return render_template("user/user_dashboard.html")



#===================
# USER Register
#===================
@bp.route("/register", methods=["GET", "POST"])
def register():


    schedule_id = request.args.get("schedule_id") # for Appointment

    if schedule_id:
        session["schedule_id"] = schedule_id

    if request.method == "GET":
        return render_template("user/user_login.html")

    fullname = request.form["fullname"].strip()
    phone = request.form["phone"].strip()
    national_code = request.form["national_code"].strip()

    if len(fullname) < 5:
        flash("لطفا نام و نام خانوادگی را کامل وارد کنید", "warning")
        return render_template(
        "user/user_login.html",
        fullname=fullname, 
        phone=phone,
        national_code=national_code
    ) # این باعث میشه اگه کاربر رمز عبور رو اشتباه زد دیگه کل اطلاعات پاک نمیشن


    if not re.fullmatch(r"(?:\+98|0)9\d{9}", phone):
        flash("شماره موبایل وارد شده صحیح نیست", "warning")
        return render_template( 
        "user/user_login.html",
        fullname=fullname,
        phone=phone,
        national_code=national_code
    )

    user_phone = User.query.filter_by(phone=phone).first()
    if user_phone :
        flash("این شماره موبایل قبلاً ثبت شده است.", "error")
        return render_template(
        "user/user_login.html",
        fullname=fullname,
        phone=phone,
        national_code=national_code
    )

    if not national_code.isdigit() or len(national_code) != 10:
        flash("کد ملی صحیح نیست", "error")
        return render_template(
        "user/user_login.html",
        fullname=fullname,
        phone=phone,
        national_code=national_code
    )
    
    
    user_national = User.query.filter_by(national_code=national_code).first()

    if user_national:
        flash("این کد ملی قبلاً ثبت شده است.", "error")
        return render_template(
            "user/user_login.html",
            fullname=fullname,
            phone=phone,
            national_code=national_code
        )

    

    otp = f"{random.randint(0, 999999):06d}" # d = integer , 6 = Number of digits , 0 : اگر کمتر از 6 رقم بود بقیه را با صفر پر کن

    session["register_data"] = {
    "fullname": fullname,
    "phone": phone,
    "national_code": national_code,
    "role": "patient"
    }

    session["otp"] = otp 
    # ذخیره زمان فعلی به اضافه 5 دقیقه
    session["otp_expire"] = (
    datetime.utcnow() + timedelta(minutes=5)).isoformat()

    print(f"OTP: {otp}") # چاپ کد تایید در ترمینال

    return redirect(url_for("user.verify"))



#===================
# USER Verify OTP
#===================
@bp.route("/verify", methods=["GET", "POST"])
def verify ():
    if request.method == "GET":
        return render_template("user/user_verify.html")

    # دریافت کد وارد شده توسط کاربر
    user_otp = request.form["user_otp"].strip()

    # بررسی صحت کد
    if user_otp != session.get("otp"):
        flash("کد تایید اشتباه است.", "error")
        return render_template("user/user_verify.html")

    # اگر کد صحیح بود
    data = session["register_data"]

    new_user = User(
        fullname=data["fullname"],
        phone=data["phone"],
        national_code=data["national_code"],
        role=data["role"]
    )

    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)

    schedule_id = session.get("schedule_id")

    if schedule_id:

        schedule = DoctorSchedule.query.get(schedule_id)

        if schedule and schedule.visit_status() != "full":

            appointment = Appointment(
                user_id=new_user.id,
                doctor_id=schedule.doctor.id,
                schedule_id=schedule.id
            )

            schedule.booked_visits += 1

            db.session.add(appointment)
            db.session.commit()


    # پاک کردن اطلاعات موقت زیرا دیگه به آنها احتیاجی نداریم
    session.pop("otp", None)
    session.pop("otp_expire", None)
    session.pop("register_data", None)
    session.pop("schedule_id", None)

    flash("با موفقیت وارد شدید.", "success")
    return redirect(url_for("user.dashboard"))




#===========================
# USER and Doctor Appointment
#===========================
@login_required
@bp.route("/appointment/<int:schedule_id>", methods=["POST"])
def appointment(schedule_id):

    schedule = DoctorSchedule.query.get_or_404(schedule_id)

    doctor = schedule.doctor

    exists = Appointment.query.filter_by(
    user_id=current_user.id,
    schedule_id=schedule.id
    ).first()

    if exists:
        flash("شما قبلاً این نوبت را رزرو کرده‌اید.", "warning")
        return redirect(url_for("user.want_doctor", id=doctor.id))

    if schedule.visit_status() == "full" :
        flash("ظرفیت این زمان تکمیل شده است.", "error")
        return redirect(url_for("user.want_doctor", id=doctor.id))

    appointment = Appointment(
    user_id=current_user.id,
    doctor_id=doctor.id,
    schedule_id=schedule.id
    )

    schedule.booked_visits += 1

    
    
    db.session.add(appointment)
    db.session.commit()

    flash("نوبت شما با موفقیت ثبت شد.", "success")
    return redirect(url_for("user.dashboard"))


#===================
# USER Logout
#===================
@login_required
@bp.route("/logout")
def logout():

    logout_user()

    flash("از حساب کاربری خارج شدید.", "success")
    return redirect(url_for("general.home"))

@bp.route("/taking_turn")
def taking_turn ():
    doctors = Doctor.query.all()
    return render_template("user/taking_turn.html", doctors=doctors)




@bp.route("/want_doctor/<int:id>")
def want_doctor(id):
    doctor = Doctor.query.get_or_404(id)
    return render_template(f"user/doctors/{doctor.template_name}", doctor=doctor) # اینجا باید بری تو فایل یوزر فایل اچ تی ام ال رو بسازی تا به این آدرس بره


# ===================================
    # روش دوم (بدون Relationship)
    # ==============================
    # schedules = DoctorSchedule.query.filter_by(
    #     doctor_id=doctor.id,
    #     active=True
    # ).all()
    #
    # return render_template(
    #     f"user/doctors/{doctor.template_name}",
    #     doctor=doctor,
    #     schedules=schedules
    # )



 # توی HTML 

    # {% for schedule in schedules %}
       
        # <p>{{ schedule.day_of_week }}</p>
        # <p>{{ schedule.start_time }}</p>
        # <p>{{ schedule.end_time }}</p>
                    
    # {% endfor %}

# ====================================


# ===================================

# ===================================