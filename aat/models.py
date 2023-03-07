from flask_sqlalchemy import SQLAlchemy
from aat.aat import app, db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    surname = db.Column(db.String)
    email = db.Column(db.String)


class Student(User):
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    course = db.Column(db.String)
    # relationship for modules
    # relationship for submissions


class Staff(User):
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    position = db.Column(db.String)
    # relationship for modules
