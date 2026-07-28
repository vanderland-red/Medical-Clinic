from flask import Blueprint,render_template,request,redirect,flash,url_for
from models.tables import User
from extentions import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user
import re



bp = Blueprint("user", __name__, url_prefix="/user")

#===================
# USER Dashboard
#===================
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
    email = request.form["email"].strip()
    password = request.form["password"]
    confirm_password = request.form["confirm_password"]

    if len(fullname) < 5:
        flash("لطفا نام و نام خانوادگی را کامل وارد کنید", "warning")
        return render_template(
        "user/user_login.html",
        fullname=fullname, 
        phone=phone,
        email=email
    ) # این باعث میشه اگه کاربر رمز عبور رو اشتباه زد دیگه کل اطلاعات پاک نمیشن


    if not re.fullmatch(r"(?:\+98|0)9\d{9}", phone):
        flash("شماره موبایل وارد شده صحیح نیست", "warning")
        return render_template( 
        "user/user_login.html",
        fullname=fullname,
        phone=phone,
        email=email
    )
    

    if len(password) == 0 :
        flash("لطفا رمز عبور خود را وارد کنید !", "warning")
        return render_template(
        "user/user_login.html",
        fullname=fullname,
        phone=phone,
        email=email
    )

    if len(password) < 5:
        flash("لطفا رمز عبور سخت تری را انتخاب کنید", "error")
        return render_template(
        "user/user_login.html",
        fullname=fullname,
        phone=phone,
        email=email
)


    if password != confirm_password:
        flash("رمز عبور و تکرار آن یکسان نیست.", "error")
        return render_template(
        "user/user_login.html",
        fullname=fullname,
        phone=phone,
        email=email
    )


    user_phone = User.query.filter_by(phone=phone).first()
    if user_phone :
        flash("این شماره موبایل قبلاً ثبت شده است.", "error")
        return redirect(url_for("user.register"))


    if email:
        user_email = User.query.filter_by(email=email).first()
        if user_email:
            flash("این ایمیل قبلاً ثبت شده است.", "error")
            return redirect(url_for("user.register"))
    else:
        email = None


    hashed_password = generate_password_hash(password)

    new_user = User(
        fullname=fullname,
        phone=phone,
        email=email,
        password=hashed_password,
        role="patient"
    )

    db.session.add(new_user)
    db.session.commit()

    flash("ثبت نام با موفقیت انجام شد.", "success")
    return redirect(url_for("user.dashboard"))


#===================
# USER Login
#===================
@bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        phone = request.form.get("phone").strip()
        password = request.form.get("password")

        user = User.query.filter_by(phone=phone).first()

        if user is None:
            flash("شماره موبایل وارد شده یافت نشد.", "error")
            return redirect(url_for("user.login"))

        if not check_password_hash(user.password, password):
            flash("رمز عبور اشتباه است.", "danger")
            return redirect(url_for("user.login"))

        login_user(user)

        flash("با موفقیت وارد حساب کاربری شدید.", "success")

        return redirect(url_for("user.dashboard"))

    return render_template("user/user_login.html")


#===================
# USER Logout
#===================
@bp.route("/logout")
def logout():

    logout_user()

    flash("از حساب کاربری خارج شدید.", "success")
    return redirect(url_for("general.home"))