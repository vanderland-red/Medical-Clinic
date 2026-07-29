from flask import Blueprint,render_template,request,redirect,flash,url_for
from models.tables import User
from extentions import db
from flask_login import login_user, login_required,current_user,logout_user
import re



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


    new_user = User(
        fullname=fullname,
        phone=phone,
        national_code=national_code,
        role="patient"
    )

    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)

    flash("با موفقیت وارد شدید", "success")
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