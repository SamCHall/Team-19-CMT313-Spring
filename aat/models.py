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
    code = db.Column(db.String, unique=True)

    user = db.relationship(
        'User',
        secondary=module_user,
        back_populates='modules'
    )

    assignments = db.relationship(
        'Assignment',
        back_populates="module"
    )

    def get_students(self):
        return [user for user in self.user if user.user_type == "student"]

    def get_staff(self):
        return [user for user in self.user if user.user_type == "staff"]


class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    module_id = db.Column(db.Integer, db.ForeignKey("module.id"))
    assignment_type = db.Column(db.String)
    active = db.Column(db.Boolean)

    module = db.relationship(
        "Module",
        back_populates="assignments"
    )

    # Questions relationship
    # Submissions relationship

    __mapper_args__ = {
        "polymorphic_on": "assignment_type",
        "polymorphic_identity": "assignment",
    }


class FormativeAssignment(Assignment):
    id = db.Column(db.Integer, db.ForeignKey("assignment.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "formative_assignment",
    }


class SummativeAssignment(Assignment):
    id = db.Column(db.Integer, db.ForeignKey("assignment.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "summative_assignment",
    }
