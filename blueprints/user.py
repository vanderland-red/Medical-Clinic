from flask import Blueprint,render_template,request,redirect,flash,url_for
from models.tables import User
from extentions import db
from werkzeug.security import generate_password_hash
import re


bp = Blueprint("user", __name__, url_prefix="/user")



@bp.route("/dashboard", methods=["GET"])
def dashboard ():
    return render_template("user/user_dashboard.html")


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
        return redirect(url_for("user.register"))


    if not re.fullmatch(r"(?:\+98|0)9\d{9}", phone):
            flash("شماره موبایل وارد شده صحیح نیست", "warning")
            return redirect(url_for("user.register"))
    

    if len(password) == 0 :
        flash("لطفا رمز عبور خود را وارد کنید !", "warning")
        return redirect(url_for("user.register"))

    if len(password) < 5:
        flash("لطفا رمز عبور سخت تری را انتخاب کنید", "error")
        return redirect(url_for("user.register"))


    if password != confirm_password:
        flash("رمز عبور و تکرار آن یکسان نیست.", "error")
        return redirect(url_for("user.register"))



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