from flask import Blueprint, render_template, redirect, url_for,request,flash
from flask_login import login_required, current_user
from models.tables import Payment, DoctorSchedule, Appointment
from extentions import db
import uuid


bp = Blueprint("payment", __name__, url_prefix="/payment")



@bp.route("/create/<int:schedule_id>")
@login_required
def create_payment(schedule_id):

    schedule = DoctorSchedule.query.get_or_404(schedule_id)


    # بررسی اینکه کاربر قبلاً این نوبت را گرفته یا نه
    exists = Appointment.query.filter_by(
        user_id=current_user.id,
        schedule_id=schedule.id
    ).first()

    if exists:
        flash("شما قبلاً این نوبت را رزرو کرده‌اید.", "warning")
        return redirect(url_for("user.doctor_details", id=schedule.doctor.id))


    # مشخصه های پرداخت شخص مورد نظر ساخته میشود
    payment = Payment(
        user_id=current_user.id,
        schedule_id=schedule.id,
        amount=schedule.doctor.visit_price,
        authority=str(uuid.uuid4()) # ساخت کد شناسه پرداخت
    )


    db.session.add(payment)
    db.session.commit()


    return redirect(url_for("payment.gateway", authority=payment.authority)) # ارسال کد شناسه پرداخت



@bp.route("/gateway/<authority>")
@login_required
def gateway(authority):

    # تایید کردن شخصی که این شناسه پرداخت را دارد 
    payment = Payment.query.filter_by(authority=authority).first_or_404()


    return render_template("payment/gateway.html", payment=payment) # ارسال اطلاعات برای استفاده از آن





#====================================================
# send information by Form in (gateway.html) page 👇
#====================================================
@bp.route("/verify/<authority>", methods=["POST"])
@login_required
def verify(authority):

    payment = Payment.query.filter_by(authority=authority).first_or_404()


    status = request.form.get("status")


    if status == "success":

        payment.status = "success"

        schedule = DoctorSchedule.query.get_or_404(payment.schedule_id)

        schedule.booked_visits += 1

        appointment = Appointment(
            doctor_id=schedule.doctor.id,
            user_id=current_user.id,
            schedule_id=payment.schedule_id,
            payment_id=payment.id
        )

        db.session.add(appointment)


    else:

        payment.status = "failed"


    db.session.commit()

    return redirect(url_for("user.dashboard"))