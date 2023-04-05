from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

from os import environ

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

    first_name = db.Column(db.String, nullable=True)
    surname = db.Column(db.String, nullable=True)
    email = db.Column(db.String, unique=True, nullable=True)
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


def create_admin() -> None:
    """Create an admin account. Should be used while initialising the app."""
    if Staff.query.filter_by(username="admin").first() == None:
        password = environ.get('ADMIN_PASSWORD') if environ.get('ADMIN_PASSWORD') != None else 'admin'
        user = Staff(username='admin', password=password, position="admin")
        db.session.add(user)
        db.session.commit()


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

    def check_student(self, student):
        """ Returns true if given student is enrolled on the module"""
        return student in self.get_students()


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

    def get_question_submissions(self, question_num):
        question = self.get_questions()[question_num]
        question_submissions = []
        for submission in self.submissions:
            for submission_answer in submission.submission_answers:
                if submission_answer.question == question:
                    question_submissions.append(submission_answer)
        return question_submissions

    def max_mark(self):
        return sum([question.max_mark() for question in self.get_questions().values()])

    def number_of_submissions(self):
        return len(self.submissions)

    def number_of_students_submitted(self):
        students = set([submission.student for submission in self.submissions])
        return len(students)

    def number_of_students_not_submitted(self):
        return len(self.module.get_students()) - self.number_of_students_submitted()

    def mark_dist(self):
        """
        Returns a dictionary for the mark distrubition of the assignment where keys and values are as follows:
            keys: the mark given
            value: the number of submissions for a given mark
        """

        marks = dict((i, 0) for i in range(self.max_mark()+1))

        for submission in self.submissions:
            marks[submission.mark] += 1

        return marks

    def lowest_mark(self):
        return min([submission.mark for submission in self.submissions])

    def highest_mark(self):
        return max([submission.mark for submission in self.submissions])

    def average_mark(self):
        return statistics.mean([submission.mark for submission in self.submissions])


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

    def get_current_attempt_number(student_id, assignment_id):
        return Submission.query.filter_by(student_id=student_id, assignment_id=assignment_id).count()

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
        if self.question_type == "question_type1":
            question_type = "Fill in the blanks"
        elif self.question_type == "question_type2":
            question_type = "Multiple choice"
        output = self.title + " | " + question_type
        return output

    @abc.abstractmethod
    def mark(self):
        pass

    @abc.abstractmethod
    def max_mark(self):
        pass

    def get_assignments(self):
        return [item.assignment for item in self.question_assignment]

    def average_mark(self, submissions = None):
        if not submissions:
            submissions = self.submissions
        return statistics.mean([submission.question_mark for submission in submissions])

    def mark_dist(self, submissions = None):
        """
        Returns a dictionary for the mark distrubition of the question where keys and values are as follows:
            keys: the mark given
            value: the number of submissions for a given mark
        """

        if not submissions:
            submissions = self.submissions

        marks = dict((i, 0) for i in range(self.max_mark()+1))

        for submission in submissions:
            marks[submission.question_mark] += 1

        sorted_by_mark = dict(sorted(marks.items()))
        return sorted_by_mark

    def marks_dist_cohort(self, submissions = None):

        if not submissions:
            submissions = self.submissions

        cohorts = set([submission.submission.student.cohort for submission in submissions])
        results = {}
        marks = list(self.mark_dist(submissions).keys())

        for cohort in cohorts:
            results[cohort] = dict((mark, 0) for mark in range(self.max_mark()+1))

        for submission in submissions:
            results[submission.submission.student.cohort][submission.question_mark] += 1

        return results

    def lowest_mark(self, submissions = None):
        if not submissions:
            submissions = self.submissions
        return min([submission.question_mark for submission in submissions])

    def highest_mark(self, submissions = None):
        if not submissions:
            submissions = self.submissions
        return max([submission.question_mark for submission in submissions])


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

    def max_mark(self):
        return self.num_of_blanks()

    def list_correct_answers(self):
        """ Method to convert the string representation of the list in the db to a list """
        return eval(self.correct_answers)

    def list_incorrect_answers(self):
        """ Method to convert the string representation of the list in the db to a list """
        return eval(self.incorrect_answers)

    def num_of_blanks(self):
        """ Method to count the number of blanks in the question """
        return len(self.list_correct_answers())

    def num_correct_for_blank(self, blank_no, submissions = None):
        """ Method to count the number of correct submissions for the given blank """
        if not submissions:
            submissions = self.submissions

        correct = 0
        for submission in submissions:
            if submission.list_submission()[blank_no] == self.list_correct_answers()[blank_no]:
                correct += 1
        return correct

    def correct_precentage_for_blank(self, blank_no, submissions = None):
        """ Method to provide the precentage of correct answers for the given blank """
        if not submissions:
            submissions = self.submissions
        return 100 * self.num_correct_for_blank(blank_no, submissions) / len(submissions)

    def answer_occur_for_blank(self, blank_no, submissions = None):
        """
        Method to produce a list of truples which contain the following
            string: A answer a student has selected for a given blank
            int: The number of submissions where they key was given as the answer to the blank

        The list is sorted with most common answers first
        """

        if not submissions:
            submissions = self.submissions

        answers = {}
        for submission in submissions:
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

    def max_mark(self):
        return 1

    def correct_submissions_number(self, submissions = None):
        if not submissions:
            submissions = self.submissions
        return sum([submission.question_mark for submission in submissions])

    def correct_submissions_percent(self, submissions = None):
        if not submissions:
            submissions = self.submissions

        if len(submissions) > 0:
            return 100 * self.correct_submissions_number(submissions) / len(submissions)
        return None

    def option_choice_quantity(self, submissions = None):
        if not submissions:
            submissions = self.submissions

        count = {
            self.option1: 0,
            self.option2: 0,
            self.option3: 0,
            self.option4: 0
        }

        for submission in submissions:
            count[submission.submission_answer] += 1

        return count
