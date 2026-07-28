from extentions import db
from datetime import datetime
from flask_login import UserMixin



class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=False)

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
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    national_code = db.Column(db.String(10), unique=True, nullable=True)
    birth_date = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(10),nullable=True)
    address = db.Column(db.Text,nullable=True)

    user = db.relationship ("User",back_populates="patient")