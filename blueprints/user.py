from flask import Blueprint,render_template


bp = Blueprint("user", __name__, url_prefix="/user")

@bp.route("/")
def login ():
    return render_template("user/user_login.html")