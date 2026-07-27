from flask import Blueprint,render_template,request,session,abort,flash,redirect,url_for
from config import ADMIN_USERNAME,ADMIN_PASSWORD


bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.before_request
def before_request() :
    if session.get("admin_login") is None and request.endpoint != "admin.login" :
        abort(403)

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



@bp.route("/logout")
def logout():
    session.pop("admin_login", None)  # حذف لاگین ادمین
    flash("با موفقیت از پنل مدیریت خارج شدید", "success")
    return redirect(url_for("admin.login"))

@bp.route("/dashboard")
def dashboard ():

    return render_template("admin/admin_dashboard.html")
