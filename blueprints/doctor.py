from flask import Blueprint,render_template
from models.tables import Appointment

bp = Blueprint("doctor", __name__, url_prefix="/doctor")

@bp.route("/dashboard")
def dashboard ():

    appointment = Appointment.query.all()
    return render_template("doctor/doctor_dashboard.html", appointment=appointment)



