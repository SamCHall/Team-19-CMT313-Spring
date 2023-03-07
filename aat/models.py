from flask_sqlalchemy import SQLAlchemy
from aat.aat import app, db


# Tables for many to many relationships links
module_user = db.Table(
    'module_user',
    db.Column("id", db.Integer, primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey('user.id')),
    db.Column("module_id", db.Integer, db.ForeignKey('module.id'))
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    surname = db.Column(db.String)
    email = db.Column(db.String)
    user_type = db.Column(db.String)

    modules = db.relationship(
        'Module',
        secondary=module_user,
        back_populates='user'
    )

    __mapper_args__ = {
        "polymorphic_on": "user_type",
        "polymorphic_identity": "user",
    }


class Student(User):
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    course = db.Column(db.String)
    cohort = db.Column(db.Integer)

    # relationship for submissions

    __mapper_args__ = {
        "polymorphic_identity": "student",
    }


class Staff(User):
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    position = db.Column(db.String)

    __mapper_args__ = {
        "polymorphic_identity": "staff",
    }


class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    code = db.Column(db.String)

    user = db.relationship(
        'User',
        secondary=module_user,
        back_populates='modules'
    )

    # relationship for assignments

    def get_students(self):
        return [user for user in self.user if user.user_type == "student"]

    def get_staff(self):
        return [user for user in self.user if user.user_type == "staff"]
