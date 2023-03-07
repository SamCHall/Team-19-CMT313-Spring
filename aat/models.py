from flask_sqlalchemy import SQLAlchemy
from aat.aat import app, db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    surname = db.Column(db.String)
    email = db.Column(db.String)
    user_type = db.Column(db.String)

    __mapper_args__ = {
        "polymorphic_on": "user_type",
        "polymorphic_identity": "user",
    }

class Student(User):
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    course = db.Column(db.String)
    cohort = db.Column(db.Integer)
    # relationship for modules
    # relationship for submissions

    __mapper_args__ = {
        "polymorphic_identity": "student",
    }

class Staff(User):
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    position = db.Column(db.String)
    # relationship for modules
    __mapper_args__ = {
        "polymorphic_identity": "staff",
    }
