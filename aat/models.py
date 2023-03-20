from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

from . import app, db
import abc
import collections
import statistics


# Tables for many to many relationships links
module_user = db.Table(
    'module_user',
    db.Column("id", db.Integer, primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey('user.id')),
    db.Column("module_id", db.Integer, db.ForeignKey('module.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    __password = db.Column(db.String, nullable=False)

    first_name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    user_type = db.Column(db.String, nullable=False)

    modules = db.relationship(
        'Module',
        secondary=module_user,
        back_populates='user'
    )

    __mapper_args__ = {
        "polymorphic_on": "user_type",
        "polymorphic_identity": "user",
    }

    @property
    def password(self):
        raise AttributeError('Password is not readable.')

    @password.setter
    def password(self,password):
        self.__password=generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.__password,password)


class Student(User):
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    course = db.Column(db.String, nullable=False)
    cohort = db.Column(db.Integer, nullable=False)

    submissions = db.relationship(
        "Submission",
        back_populates = "student"
    )

    __mapper_args__ = {
        "polymorphic_identity": "student",
    }


class Staff(User):
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    position = db.Column(db.String, nullable=False)

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
    def __str__(self):
        return (self.code).upper() + " " + self.name

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

    question_assignment = db.relationship(
        "AssignQuestion",
        back_populates = "assignment",
        order_by = "AssignQuestion.question_number.asc()"
    )

    submissions = db.relationship(
        "Submission",
        back_populates = "assignment"
    )

    __mapper_args__ = {
        "polymorphic_on": "assignment_type",
        "polymorphic_identity": "assignment",
    }

    def get_questions(self):
        return dict([(item.question_number, item.question) for item in self.question_assignment])

    def add_question(self, question, question_no):
        return AssignQuestion.add_question(self.id, question.id, question_no)


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


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey("assignment.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)

    attempt_number = db.Column(db.Integer, nullable=False)
    mark = db.Column(db.Integer, nullable=False)

    assignment = db.relationship(
        "Assignment",
        back_populates = "submissions"
    )

    student = db.relationship(
        "Student",
        back_populates = "submissions"
    )

    submission_answers = db.relationship(
        "SubmissionAnswers",
        back_populates = "submission"
    )

    def add_question_answer(self, question, answer, mark):
        if question.question_type == "question_type1":
            question_submission = SubmissionType1(
                question = question,
                submission = self,
                submission_answer = answer,
                question_mark = mark
            )
            db.session.add(question_submission)
            db.session.commit()

        elif question.question_type == "question_type2":
            question_submission = SubmissionType2(
                question = question,
                submission = self,
                submission_answer = answer,
                question_mark = mark
            )
            db.session.add(question_submission)
            db.session.commit()


class SubmissionAnswers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"), nullable=False)
    submission_id = db.Column(db.Integer, db.ForeignKey("submission.id"), nullable=False)
    submission_question_type = db.Column(db.String)
    question_mark = db.Column(db.Integer, nullable=False)

    question = db.relationship(
        "Question",
        back_populates = "submissions"
    )

    submission = db.relationship(
        "Submission",
        back_populates = "submission_answers"
    )

    __mapper_args__ = {
        "polymorphic_on": "submission_question_type",
        "polymorphic_identity": "submission",
    }


class SubmissionType1(SubmissionAnswers):
    id = db.Column(db.Integer, db.ForeignKey("submission_answers.id"), primary_key=True)
    submission_answer = db.Column(db.String, nullable=False)

    def list_submission(self):
        return eval(self.submission_answer)

    __mapper_args__ = {
        "polymorphic_identity": "submission_type1",
    }


class SubmissionType2(SubmissionAnswers):
    id = db.Column(db.Integer, db.ForeignKey("submission_answers.id"), primary_key=True)
    submission_answer = db.Column(db.String, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "submission_type2",
    }


class AssignQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey("assignment.id"))
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"))
    question_number = db.Column(db.Integer)

    assignment = db.relationship(
        "Assignment",
        back_populates = "question_assignment"
    )

    question = db.relationship(
        "Question",
        back_populates = "question_assignment"
    )

    @staticmethod
    def get_assignment_questions(assignment_id):
        assign = AssignQuestion.query.filter_by(assignment_id=assignment_id).order_by(AssignQuestion.question_number.asc()).all()
        questions = dict([(item.question_number, item.question) for item in assign])
        return questions

    @staticmethod
    def get_question_assignments(question_id):
        assign = AssignQuestion.query.filter_by(question_id=question_id).all()
        assignments = [item.assignment for item in assign]
        return assignments

    @staticmethod
    def add_question(assignment_id, question_id, question_number):
        print(assignment_id, question_id, question_number)
        assign = AssignQuestion(
            assignment_id = assignment_id,
            question_id = question_id,
            question_number = question_number
        )
        db.session.add(assign)
        db.session.commit()


# https://stackoverflow.com/a/28727066/
class QuestionMeta(type(db.Model), type(abc.ABC)):
    pass


class Question(db.Model, abc.ABC, metaclass=QuestionMeta):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, unique=True)
    question_type = db.Column(db.String)
    active = db.Column(db.Boolean, default=False)

    question_assignment = db.relationship(
        "AssignQuestion",
        back_populates = "question"
    )

    submissions = db.relationship(
        "SubmissionAnswers",
        back_populates = "question"
    )

    __mapper_args__ = {
        "polymorphic_on": "question_type",
        "polymorphic_identity": "question",
    }

    def __str__(self):
        output = self.title + " " + self.question_type
        return output

    @abc.abstractmethod
    def mark(self):
        pass

    def get_assignments(self):
        return [item.assignment for item in self.question_assignment]

    def average_mark(self):
        return statistics.mean([submission.question_mark for submission in self.submissions])

    def mark_dist(self):
        """
        Returns a dictionary for the mark distrubition of the question where keys and values are as follows:
            keys: the mark given
            value: the number of submissions for a given mark
        """

        marks = {}

        for submission in self.submissions:
            if submission.question_mark in marks:
                marks[submission.question_mark] += 1
            else:
                marks[submission.question_mark] = 1

        sorted_by_mark = dict(sorted(marks.items()))
        return sorted_by_mark

    def lowest_mark(self):
        return min(list(self.mark_dist().keys()))

    def highest_mark(self):
        return max(list(self.mark_dist().keys()))


class QuestionType1(Question):
    """Fill in the blank."""
    id = db.Column(db.Integer, db.ForeignKey("question.id"), primary_key=True)
    question_template = db.Column(db.String, nullable=False)
    correct_answers = db.Column(db.String, nullable=False)
    incorrect_answers = db.Column(db.String)

    __mapper_args__ = {
        "polymorphic_identity": "question_type1",
    }

    def mark(self):
        return 0

    def list_correct_answers(self):
        """ Method to convert the string representation of the list in the db to a list """
        return eval(self.correct_answers)

    def list_incorrect_answers(self):
        """ Method to convert the string representation of the list in the db to a list """
        return eval(self.incorrect_answers)

    def num_of_blanks(self):
        """ Method to count the number of blanks in the question """
        return len(self.list_correct_answers())

    def num_correct_for_blank(self, blank_no):
        """ Method to count the number of correct submissions for the given blank """
        correct = 0
        for submission in self.submissions:
            if submission.list_submission()[blank_no] == self.list_correct_answers()[blank_no]:
                correct += 1
        return correct

    def correct_precentage_for_blank(self, blank_no):
        """ Method to provide the precentage of correct answers for the given blank """
        return 100 * self.num_correct_for_blank(blank_no) / len(self.submissions)

    def answer_occur_for_blank(self, blank_no):
        """
        Method to produce a list of truples which contain the following
            string: A answer a student has selected for a given blank
            int: The number of submissions where they key was given as the answer to the blank

        The list is sorted with most common answers first
        """

        answers = {}
        for submission in self.submissions:
            if (answer:= submission.list_submission()[blank_no]) in answers.keys():
                answers[answer] += 1
            else:
                answers[answer] = 1
        # https://stackoverflow.com/a/11230132
        sorted_answers = collections.Counter(answers).most_common()
        return sorted_answers


class QuestionType2(Question):
    id = db.Column(db.Integer, db.ForeignKey("question.id"), primary_key=True)
    question_text = db.Column(db.String)
    option1 = db.Column(db.String)
    option2 = db.Column(db.String)
    option3 = db.Column(db.String)
    option4 = db.Column(db.String)
    correctOption = db.Column(db.String)

    __mapper_args__ = {
        "polymorphic_identity": "question_type2",
    }

    def mark(self):
        return 0
