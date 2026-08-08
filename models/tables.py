from extentions import db
from datetime import datetime
from flask_login import UserMixin



class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), nullable=False)
    national_code = db.Column(db.String(10), nullable=False)

    role = db.Column(
        db.Enum("patient", "doctor", "admin", name="user_roles"),
        nullable=False,
        default="patient"
    )

    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # One to Many
    appointments = db.relationship("Appointment", back_populates="user")




class Doctor(db.Model):
    __tablename__ = "doctors"

    id = db.Column(db.Integer, primary_key=True)
    doctor_name = db.Column(db.String(100), nullable=False)
    experience_years = db.Column(db.Integer, nullable=False)
    biography = db.Column(db.Text, nullable=True)
    visit_price = db.Column(db.Integer, nullable=False)
    profile_image = db.Column(db.String(255), nullable=True)
    specials = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(11), unique=True, nullable=False)
    password = db.Column(db.String(255)) 

    # One to Many
    schedules = db.relationship("DoctorSchedule", back_populates="doctor", cascade="all, delete-orphan")

    # One to Many
    appointments = db.relationship("Appointment",back_populates="doctor")





class DoctorSchedule(db.Model):
    __tablename__ = "doctor_schedule"

    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"), nullable=False)
    day_of_week = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    max_visits = db.Column(db.Integer, nullable=False)
    booked_visits = db.Column(db.Integer, default=0, nullable=False)

    # One to Many
    doctor = db.relationship("Doctor", back_populates="schedules")

    appointments = db.relationship("Appointment",back_populates="schedule")

    def visit_status(self):
        if self.booked_visits >= self.max_visits :
            return "full"
        return "allowed"



# اتصاب دادن بین دکتر و یوزر
class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"), nullable=False)
    schedule_id = db.Column(db.Integer, db.ForeignKey("doctor_schedule.id"), nullable=False)
    payment_id = db.Column(db.Integer, db.ForeignKey("payments.id"), nullable=False, unique=True)
    status = db.Column(db.Enum("pending", "accepted", "rejected", "done"), default="pending", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Many to One
    user = db.relationship("User", back_populates="appointments")
    doctor = db.relationship("Doctor", back_populates="appointments")
    schedule = db.relationship("DoctorSchedule", back_populates="appointments")
    payment = db.relationship("Payment", back_populates="appointment")





class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"),nullable=False)
    schedule_id = db.Column(db.Integer,db.ForeignKey("doctor_schedule.id"),nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    authority = db.Column(db.String(100),unique=True)
    status = db.Column(db.String(20), default="pending")
    created_at = db.Column(db.DateTime,default=datetime.utcnow)


    user = db.relationship("User", backref="payments")
    schedule = db.relationship("DoctorSchedule", backref="payments")
    appointment = db.relationship("Appointment", back_populates="payment", uselist=False)