from . import db
from .models import *

if User.query.first() is None:
    student1 = Student(
        username = "rtjst",
        password = "alpha",
        email = "c@example.com",
        first_name = "Alpha",
        surname = "1",
        cohort = 2013,
        course = "computing",
    )
    db.session.add(student1)

    student2 = Student(
        username = "ej7u6s",
        password = "alpha",
        email = "d@example.com",
        first_name = "Beta",
        surname = "2",
        cohort = 2013,
        course = "computing"
    )
    db.session.add(student2)

    student3 = Student(
        username = "dhtrh",
        password = "alpha",
        email = "e@example.com",
        first_name = "Gamma",
        surname = "3",
        cohort = 2014,
        course = "computing"
    )
    db.session.add(student3)

    student4 = Student(
        username = "dtyhstre",
        password = "alpha",
        email = "f@example.com",
        first_name = "Delta",
        surname = "4",
        cohort = 2014,
        course = "computing"
    )
    db.session.add(student4)

    staff1 = Staff(
        username = "dttrhyt",
        password = "alpha",
        email = "a@example.com",
        first_name = "Martin",
        surname = "Chorley",
        position = "Lect"
    )
    db.session.add(staff1)

    staff2 = Staff(
        username = "ujytyd",
        password = "alpha",
        email = "b@example.com",
        first_name = "Matthew",
        surname = "Morgan",
        position = "Lect"
    )
    db.session.add(staff2)

    module1 = Module(
        name = "Computational Thinking",
        code = "CMT119",
        user = [student1, student2, student3, staff1, staff2]
    )
    db.session.add(module1)

    module2 = Module(
        name = "Fundamentals of Programming",
        code = "CMT120",
        user = [student1, student2, student4, staff1]
    )
    db.session.add(module2)

    q1 = QuestionType1(
        title = "hi",
        question_template = "A {} language program is called {} code.",
        correct_answers = "['high-level', ' source']",
    )
    db.session.add(q1)

    q2 = QuestionType1(
        title = "hello",
        question_template = "A {} translates source code into {} code.",
        correct_answers = "['compiler', ' object']",
    )
    db.session.add(q2)

    q3 = QuestionType1(
        title = "world",
        question_template = "An {} analyses each {} of the {} code as it {} the statement.",
        correct_answers = "['interpreter', 'statement', 'source, 'executes']",
    )
    db.session.add(q3)

    q4 = QuestionType2(
        title = "hi2"
    )
    db.session.add(q4)

    q5 = QuestionType2(
        title = "hello2"
    )
    db.session.add(q5)

    q6 = QuestionType2(
        title = "world2"
    )
    db.session.add(q6)

    assignment1 = SummativeAssignment(
        title = "Html & Css Based Assessment ",
        module = module1,
        active = True
    )
    db.session.add(assignment1)

    assignment2 = SummativeAssignment(
        title = "Programming Challenges",
        module = module2,
        active = True
    )
    db.session.add(assignment2)

    assignment3 = SummativeAssignment(
        title = "Web Application Development",
        module = module2,
        active = True
    )
    db.session.add(assignment3)

    assignment4 = FormativeAssignment(
        title = "Variables - Quiz",
        module = module1,
        active = True
    )
    db.session.add(assignment4)

    assignment5 = FormativeAssignment(
        title = "Statements, Expressions and Operators - Quiz",
        module = module1,
        active = True
    )
    db.session.add(assignment5)

    assignment6 = FormativeAssignment(
        title = "Iteration - Quiz",
        module = module1,
        active = True
    )
    db.session.add(assignment6)

    db.session.commit()

    assignment1.add_question(q1, 1)
    assignment1.add_question(q2, 3)
    assignment1.add_question(q3, 2)

    db.session.commit()
    print("Test data has been added to the database.")

else:
    print("Database already contains data, test data has not been added.")
