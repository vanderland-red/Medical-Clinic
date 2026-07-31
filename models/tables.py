from extentions import db
from datetime import datetime
from flask_login import UserMixin



class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    national_code = db.Column(db.String(10), unique=True, nullable=False)

    role = db.Column(
        db.Enum("patient", "doctor", "admin", name="user_roles"),
        nullable=False,
        default="patient"
    )

    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # One to One 
    patient = db.relationship(
    "Patient",
    back_populates="user",
    uselist=False,
    cascade="all, delete-orphan"
    )




class Patient(db.Model):

    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(10),nullable=True)
    address = db.Column(db.Text,nullable=True)

    # One to One
    user = db.relationship ("User",back_populates="patient")




class Doctor(db.Model):
    __tablename__ = "doctors"

    id = db.Column(db.Integer, primary_key=True)
    doctor_name = db.Column(db.String(100), nullable=False)
    experience_years = db.Column(db.Integer, nullable=False)
    biography = db.Column(db.Text, nullable=True)
    visit_price = db.Column(db.Integer, nullable=False)
    profile_image = db.Column(db.String(255), nullable=True)
    specials = db.Column(db.String(200), nullable=False)
    template_name = db.Column(db.String(100)) 

    # One to Many
    schedules = db.relationship("DoctorSchedule", back_populates="doctor", cascade="all, delete-orphan")




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

    def visit_status(self):
        if self.booked_visits >= self.max_visits :
            return "full"
        return "allowed"



