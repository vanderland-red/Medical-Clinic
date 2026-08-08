from flask import Blueprint,render_template,request,redirect,flash,url_for
from models.tables import User,Doctor,DoctorSchedule,Appointment,Payment
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
    appointment = Appointment.query.filter_by(user_id=current_user.id).all()
    return render_template("user/user_dashboard.html", appointment=appointment)



#===================
# USER Register
#===================
@bp.route("/register", methods=["GET", "POST"])
def register():


    schedule_id = request.args.get("schedule_id") # انتخاب دکتر مورد نظر

    if schedule_id:
        session["schedule_id"] = schedule_id

    if request.method == "GET":
        return render_template("user/user_login.html")

    phone = request.form["phone"].strip()
    national_code = request.form["national_code"].strip()


    if not re.fullmatch(r"(?:\+98|0)9\d{9}", phone):
        flash("شماره موبایل وارد شده صحیح نیست", "warning")
        return render_template( 
        "user/user_login.html",
        phone=phone,
        national_code=national_code
    ) # این باعث میشه اگه کاربر رمز عبور رو اشتباه زد دیگه کل اطلاعات پاک نمیشن


    if not national_code.isdigit() or len(national_code) != 10:
        flash("کد ملی صحیح نیست", "error")
        return render_template(
        "user/user_login.html",
        phone=phone,
        national_code=national_code
    )
    
    

    

    otp = f"{random.randint(0, 999999):06d}" # d = integer , 6 = Number of digits , 0 : اگر کمتر از 6 رقم بود بقیه را با صفر پر کن

    session["register_data"] = {
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



#=============================
# USER Register Verify OTP
#=============================
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

    user = User.query.filter_by(
        phone=data["phone"],
        national_code=data["national_code"]
    ).first()

    if user :
        login_user(user)

        schedule_id = session.get("schedule_id")
        
        if schedule_id:
            return redirect(url_for("payment.create_payment", schedule_id=schedule_id))

    else :
        user = User(
            phone=data["phone"],
            national_code=data["national_code"],
            role=data["role"]
        )

        db.session.add(user)
        db.session.commit()

        login_user(user)

        # پاک کردن اطلاعات موقت زیرا دیگه به آنها احتیاجی نداریم

        session.pop("otp", None)
        session.pop("otp_expire", None)
        session.pop("register_data", None)

        schedule_id = session.get("schedule_id")

        if schedule_id:

            return redirect(url_for("payment.create_payment", schedule_id=schedule_id))






#=====================================
# USER LOGIN for going to dashboard
#=====================================
@bp.route("/login", methods=["GET", "POST"])
def login_this():


    if request.method == "GET" :
        return render_template("user/user_login_this.html")
    
    phone = request.form.get("phone")

    if not re.fullmatch(r"(?:\+98|0)9\d{9}", phone):
        flash("شماره موبایل وارد شده صحیح نیست", "warning")
        return redirect(url_for("user.login_this"))

    phone_exit = User.query.filter_by(phone=phone).first()

    if phone_exit is None :
        flash("شماره موبایل مورد نظر یافت نشد !", "error")
        return redirect(url_for("user.login_this"))

    otp = f"{random.randint(0, 999999):06d}"

    session["login_data"] = {
    "phone": phone
    }

    session["otp"] = otp 
    # ذخیره زمان فعلی به اضافه 5 دقیقه
    session["otp_expire"] = (
    datetime.utcnow() + timedelta(minutes=5)).isoformat()

    print(f"OTP: {otp}") # چاپ کد تایید در ترمینال

    return redirect(url_for("user.verify_login"))



#================================================
# USER LOGIN Verify OTP for going to dashboard
#================================================
@bp.route("/verify-user-login", methods=["GET", "POST"])
def verify_login ():
    if request.method == "GET":
        return render_template("user/user_verify_this.html")

    
    user_otp = request.form["user_otp"].strip()
    
    # بررسی صحت کد
    if user_otp != session.get("otp"):
        flash("کد تایید اشتباه است.", "error")
        return redirect(url_for("user.verify_login"))

    phone = session["login_data"]["phone"]

    user_login = User.query.filter_by(phone=phone).first()

    # یا به این روش هم میشه دیتا ذخیره کرد
    # data = session["login_data"]
    # user_login = User.query.filter_by(phone=data["phone"]).first()

    if user_login is None:
        flash("کاربر یافت نشد.", "error")
        return redirect(url_for("user.login_this"))

    login_user(user_login)

    session.pop("otp", None)
    session.pop("otp_expire", None)
    session.pop("login_data", None)

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

    schedule_id = session.get("schedule_id")


    if schedule_id:

        return redirect(url_for("payment.create_payment", schedule_id=schedule_id))

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
    doctors = Doctor.query.join(Doctor.schedules)\
    .filter(DoctorSchedule.active == 1)\
    .all()
    return render_template("user/taking_turn.html", doctors=doctors)




@bp.route("/doctor_details/<int:id>")
def doctor_details(id):
    doctor = Doctor.query.get_or_404(id) # اطلاعات دکتر مورد نظر
    schedule = DoctorSchedule.query.filter_by(doctor_id=id).all() # برنامه کاری دکتر مورد نظر
    return render_template("user/doctor_details.html", doctor=doctor, schedule=schedule)

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
# USER Schedule Delete
# ===================================
@bp.route("/schedule_delete/<int:id>", methods=["POST"])
def schedule_delete(id):

    item = Appointment.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first_or_404()

    item.schedule.booked_visits -= 1

    db.session.delete(item)
    db.session.commit()

    flash("نوبت با موفقیت حذف شد", "success")
    return redirect(url_for("user.dashboard"))


