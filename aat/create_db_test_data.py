from . import db
from .models import *

if User.query.count() <= 1:
    student1 = Student(
        username = "leia",
        password = "alpha",
        email = "c@example.com",
        first_name = "Leia",
        surname = "Beasley",
        cohort = 2013,
        course = "computing",
    )
    db.session.add(student1)

    student2 = Student(
        username = "priya",
        password = "alpha",
        email = "d@example.com",
        first_name = "Priya",
        surname = "Bishop",
        cohort = 2013,
        course = "computing"
    )
    db.session.add(student2)

    student3 = Student(
        username = "elliot",
        password = "alpha",
        email = "e@example.com",
        first_name = "Elliot",
        surname = "Hull",
        cohort = 2014,
        course = "computing"
    )
    db.session.add(student3)

    student4 = Student(
        username = "nathaniel",
        password = "alpha",
        email = "f@example.com",
        first_name = "Nathaniel",
        surname = "Moore",
        cohort = 2014,
        course = "computing"
    )
    db.session.add(student4)

    student5 = Student(
        username = "alexandria",
        password = "alpha",
        email = "g@example.com",
        first_name = "Alexandria",
        surname = "Wolf",
        cohort = 2013,
        course = "computing",
    )
    db.session.add(student1)

    student6 = Student(
        username = "jada",
        password = "alpha",
        email = "h@example.com",
        first_name = "Jada",
        surname = "Le",
        cohort = 2014,
        course = "computing"
    )
    db.session.add(student2)

    student7 = Student(
        username = "kristina",
        password = "alpha",
        email = "i@example.com",
        first_name = "Kristina",
        surname = "Knowles",
        cohort = 2014,
        course = "computing"
    )
    db.session.add(student3)

    student8 = Student(
        username = "eesa",
        password = "alpha",
        email = "j@example.com",
        first_name = "Eesa",
        surname = "Ray",
        cohort = 2014,
        course = "computing"
    )
    db.session.add(student4)

    staff1 = Staff(
        username = "elena",
        password = "alpha",
        email = "a@example.com",
        first_name = "Elena",
        surname = "Thomas",
        position = "Lect"
    )
    db.session.add(staff1)

    staff2 = Staff(
        username = "oakley",
        password = "alpha",
        email = "b@example.com",
        first_name = "Oakley",
        surname = "Bender",
        position = "Lect"
    )
    db.session.add(staff2)

    module1 = Module(
        name = "Programming",
        code = "COMP1-2",
        user = [student1, student2, student3, staff1, staff2]
    )
    db.session.add(module1)

    module2 = Module(
        name = "Computer systems",
        code = "COMP2-8",
        user = [student1, student2, student3, student4, student5, student6, student7, student8, staff1, staff2]
    )
    db.session.add(module2)

    module3 = Module(
        name = "The Internet",
        code = "COMP2-9",
        user = [student1, student2, student4, staff1]
    )
    db.session.add(module3)

    q1 = QuestionType1(
        title = "Programming Language 1",
        active = True,
        question_template = "A {} language program is called {} code.",
        correct_answers = "['high-level', 'source']",
        incorrect_answers = "['high', 'low', 'low-level', 'machine', 'object', 'assembly']"
    )
    db.session.add(q1)

    q2 = QuestionType1(
        title = "Translator 1",
        active = True,
        question_template = "A {} translates source code into {} code.",
        correct_answers = "['compiler', 'object']",
        incorrect_answers = "['interpreter', 'assemblers', 'executes', 'machine', 'source']"
    )
    db.session.add(q2)

    q3 = QuestionType1(
        title = "Running software 1",
        active = True,
        question_template = "An {} analyses each {} of the {} code as it {} the statement.",
        correct_answers = "['interpreter', 'statement', 'source', 'executes']",
        incorrect_answers = "['compiler', 'assemblers', 'machine', 'object', 'assembly', 'line']"
    )
    db.session.add(q3)

    q4 = QuestionType2(
        title = "Application Software 1",
        question_text = "Which of the following is not a type of application software?",
        option1 = "Bespoke application software",
        option2 = "General purpose software",
        option3 = "Multi purpose software",
        option4 = "Special purpose software",
        correctOption = "Multi purpose software"
    )
    db.session.add(q4)

    q5 = QuestionType2(
        title = "Application Software 2",
        question_text = "Which of the following is a application software?",
        option1 = "Video games",
        option2 = "Utility programs",
        option3 = "Operating Systems",
        option4 = "Translator software",
        correctOption = "Video games"
    )
    db.session.add(q5)

    q6 = QuestionType2(
        title = "Hardware 1",
        question_text = "Which of the following is internal component?",
        option1 = "Mouse",
        option2 = "Processor",
        option3 = "Monitor",
        option4 = "Keyboard",
        correctOption = "Processor"
    )
    db.session.add(q6)

    assignment1 = SummativeAssignment(
        title = "Procedures and functions",
        module = module1,
        active = True
    )
    db.session.add(assignment1)

    assignment2 = FormativeAssignment(
        title = "Hardware devices",
        module = module2,
        active = True
    )
    db.session.add(assignment2)

    assignment3 = SummativeAssignment(
        title = "Web site design",
        module = module3,
        active = True
    )
    db.session.add(assignment3)

    assignment4 = FormativeAssignment(
        title = "Classification of software",
        module = module2,
        active = True
    )
    db.session.add(assignment4)

    assignment5 = FormativeAssignment(
        title = "Structure of the Internet",
        module = module3,
        active = True
    )
    db.session.add(assignment5)

    assignment6 = FormativeAssignment(
        title = "Data types",
        module = module1,
        active = True
    )
    db.session.add(assignment6)

    assignment7 = FormativeAssignment(
        title = "All Questions Formative",
        module = module2,
        active = True
    )
    db.session.add(assignment7)

    assignment8 = FormativeAssignment(
        title = "COMP2-8 All",
        module = module2,
        active = True
    )
    db.session.add(assignment8)

    db.session.commit()

    assignment2.add_question(q6, 1)

    assignment4.add_question(q1, 1)
    assignment4.add_question(q2, 5)
    assignment4.add_question(q3, 3)
    assignment4.add_question(q4, 2)
    assignment4.add_question(q5, 4)

    assignment7.add_question(q1, 1)
    assignment7.add_question(q2, 2)
    assignment7.add_question(q3, 3)
    assignment7.add_question(q4, 4)
    assignment7.add_question(q5, 5)
    assignment7.add_question(q6, 6)

    assignment8.add_question(q1, 1)
    assignment8.add_question(q2, 5)
    assignment8.add_question(q3, 3)
    assignment8.add_question(q4, 2)
    assignment8.add_question(q5, 4)
    assignment8.add_question(q6, 6)

    submission1 = Submission(
        assignment = assignment4,
        student = student1,
        attempt_number = 1,
        mark = 7
    )
    db.session.add(submission1)
    submission1.add_question_answer(q1, "['low-level', 'source']", 1)
    submission1.add_question_answer(q2, "['compiler', 'object']", 2)
    submission1.add_question_answer(q3, "['interpreter', 'line', 'source', 'executes']", 3)
    submission1.add_question_answer(q4, "Multi purpose software", 1)
    submission1.add_question_answer(q5, "Translator software", 0)

    submission2 = Submission(
        assignment = assignment4,
        student = student2,
        attempt_number = 1,
        mark = 10
    )
    db.session.add(submission2)
    submission2.add_question_answer(q1, "['high-level', 'source']", 2)
    submission2.add_question_answer(q2, "['compiler', 'object']", 2)
    submission2.add_question_answer(q3, "['interpreter', 'statement', 'source', 'executes']", 4)
    submission2.add_question_answer(q4, "Multi purpose software", 1)
    submission2.add_question_answer(q5, "Video games", 1)

    submission3 = Submission(
        assignment = assignment4,
        student = student4,
        attempt_number = 1,
        mark = 2
    )
    db.session.add(submission1)
    submission3.add_question_answer(q1, "['high-level', 'object']", 1)
    submission3.add_question_answer(q2, "['interpreter', 'source']", 0)
    submission3.add_question_answer(q3, "['compiler', 'line', 'machine', 'executes']", 1)
    submission3.add_question_answer(q4, "General purpose software", 0)
    submission3.add_question_answer(q5, "Utility programs", 0)

    submission4 = Submission(
        assignment = assignment4,
        student = student5,
        attempt_number = 1,
        mark = 3
    )
    db.session.add(submission4)
    submission4.add_question_answer(q1, "['high', 'object']", 0)
    submission4.add_question_answer(q2, "['assemblers', 'machine']", 0)
    submission4.add_question_answer(q3, "['interpreter', 'line', 'object', 'executes']", 2)
    submission4.add_question_answer(q4, "Special purpose software", 0)
    submission4.add_question_answer(q5, "Video games", 1)

    submission5 = Submission(
        assignment = assignment4,
        student = student6,
        attempt_number = 1,
        mark = 7
    )
    db.session.add(submission5)
    submission5.add_question_answer(q1, "['high-level', 'source']", 2)
    submission5.add_question_answer(q2, "['interpreter', 'object']", 1)
    submission5.add_question_answer(q3, "['compiler', 'statement', 'assembly', 'executes']", 2)
    submission5.add_question_answer(q4, "Multi purpose software", 1)
    submission5.add_question_answer(q5, "Video games", 1)

    submission6 = Submission(
        assignment = assignment4,
        student = student7,
        attempt_number = 1,
        mark = 6
    )
    db.session.add(submission6)
    submission6.add_question_answer(q1, "['high-level', 'assembly']", 1)
    submission6.add_question_answer(q2, "['compiler', 'source']", 1)
    submission6.add_question_answer(q3, "['compiler', 'statement', 'machine', 'executes']", 2)
    submission6.add_question_answer(q4, "Multi purpose software", 1)
    submission6.add_question_answer(q5, "Video games", 1)

    submission7 = Submission(
        assignment = assignment2,
        student = student1,
        attempt_number = 1,
        mark = 0
    )
    db.session.add(submission7)
    submission7.add_question_answer(q6, "Mouse", 0)

    submission8 = Submission(
        assignment = assignment2,
        student = student2,
        attempt_number = 1,
        mark = 1
    )
    db.session.add(submission8)
    submission8.add_question_answer(q6, "Processor", 1)

    submission9 = Submission(
        assignment = assignment2,
        student = student3,
        attempt_number = 1,
        mark = 0
    )
    db.session.add(submission9)
    submission9.add_question_answer(q6, "Monitor", 0)

    submission10 = Submission(
        assignment = assignment2,
        student = student4,
        attempt_number = 1,
        mark = 1
    )
    db.session.add(submission10)
    submission10.add_question_answer(q6, "Processor", 1)

    submission11 = Submission(
        assignment = assignment2,
        student = student5,
        attempt_number = 1,
        mark = 1
    )
    db.session.add(submission11)
    submission11.add_question_answer(q6, "Processor", 1)

    submission12 = Submission(
        assignment = assignment2,
        student = student6,
        attempt_number = 1,
        mark = 1
    )
    db.session.add(submission12)
    submission12.add_question_answer(q6, "Processor", 1)

    submission13 = Submission(
        assignment = assignment2,
        student = student7,
        attempt_number = 1,
        mark = 0
    )
    db.session.add(submission13)
    submission13.add_question_answer(q6, "Monitor", 0)

    submission14 = Submission(
        assignment = assignment8,
        student = student1,
        attempt_number = 1,
        mark = 11
    )
    db.session.add(submission14)
    submission14.add_question_answer(q1, "['high-level', 'source']", 2)
    submission14.add_question_answer(q2, "['compiler', 'object']", 2)
    submission14.add_question_answer(q3, "['interpreter', 'statement', 'source', 'executes']", 4)
    submission14.add_question_answer(q4, "Multi purpose software", 1)
    submission14.add_question_answer(q5, "Video games", 1)
    submission14.add_question_answer(q6, "Processor", 1)

    submission15 = Submission(
        assignment = assignment8,
        student = student2,
        attempt_number = 1,
        mark = 11
    )
    db.session.add(submission15)
    submission15.add_question_answer(q1, "['high-level', 'source']", 2)
    submission15.add_question_answer(q2, "['compiler', 'object']", 2)
    submission15.add_question_answer(q3, "['interpreter', 'statement', 'source', 'executes']", 4)
    submission15.add_question_answer(q4, "Multi purpose software", 1)
    submission15.add_question_answer(q5, "Video games", 1)
    submission15.add_question_answer(q6, "Processor", 1)

    submission16 = Submission(
        assignment = assignment8,
        student = student3,
        attempt_number = 1,
        mark = 9
    )
    db.session.add(submission16)
    submission16.add_question_answer(q1, "['low-level', 'source']", 1)
    submission16.add_question_answer(q2, "['compiler', 'object']", 2)
    submission16.add_question_answer(q3, "['interpreter', 'statement', 'source', 'executes']", 4)
    submission16.add_question_answer(q4, "Multi purpose software", 1)
    submission16.add_question_answer(q5, "Video games", 1)
    submission16.add_question_answer(q6, "Keyboard", 0)

    submission17 = Submission(
        assignment = assignment8,
        student = student4,
        attempt_number = 1,
        mark = 6
    )
    db.session.add(submission17)
    submission17.add_question_answer(q1, "['high-level', 'source']", 2)
    submission17.add_question_answer(q2, "['interpreter', 'object']", 1)
    submission17.add_question_answer(q3, "['compiler', 'line', 'source', 'executes']", 2)
    submission17.add_question_answer(q4, "General purpose software", 0)
    submission17.add_question_answer(q5, "Translator software", 0)
    submission17.add_question_answer(q6, "Processor", 1)

    submission18 = Submission(
        assignment = assignment8,
        student = student5,
        attempt_number = 1,
        mark = 7
    )
    db.session.add(submission18)
    submission18.add_question_answer(q1, "['high-level', 'source']", 2)
    submission18.add_question_answer(q2, "['interpreter', 'object']", 1)
    submission18.add_question_answer(q3, "['assemblers', 'line', 'source', 'executes']", 2)
    submission18.add_question_answer(q4, "Multi purpose software", 1)
    submission18.add_question_answer(q5, "Translator software", 0)
    submission18.add_question_answer(q6, "Processor", 1)

    submission19 = Submission(
        assignment = assignment8,
        student = student6,
        attempt_number = 1,
        mark = 6
    )
    db.session.add(submission19)
    submission19.add_question_answer(q1, "['high-level', 'object']", 1)
    submission19.add_question_answer(q2, "['assemblers', 'object']", 1)
    submission19.add_question_answer(q3, "['interpreter', 'statement', 'object', 'executes']", 3)
    submission19.add_question_answer(q4, "Special purpose software", 0)
    submission19.add_question_answer(q5, "Utility programs", 0)
    submission19.add_question_answer(q6, "Processor", 1)

    submission20 = Submission(
        assignment = assignment8,
        student = student7,
        attempt_number = 1,
        mark = 8
    )
    db.session.add(submission20)
    submission20.add_question_answer(q1, "['high-level', 'object']", 1)
    submission20.add_question_answer(q2, "['assemblers', 'object']", 1)
    submission20.add_question_answer(q3, "['interpreter', 'statement', 'object', 'executes']", 3)
    submission20.add_question_answer(q4, "Multi purpose software", 1)
    submission20.add_question_answer(q5, "Video games", 1)
    submission20.add_question_answer(q6, "Processor", 1)

    submission21 = Submission(
        assignment = assignment8,
        student = student8,
        attempt_number = 1,
        mark = 10
    )
    db.session.add(submission20)
    submission21.add_question_answer(q1, "['high-level', 'source']", 2)
    submission21.add_question_answer(q2, "['compiler', 'object']", 2)
    submission21.add_question_answer(q3, "['interpreter', 'statement', 'object', 'executes']", 3)
    submission21.add_question_answer(q4, "Multi purpose software", 1)
    submission21.add_question_answer(q5, "Video games", 1)
    submission21.add_question_answer(q6, "Processor", 1)

    db.session.commit()
    print("Test data has been added to the database.")

else:
    print("Database already contains data, test data has not been added.")
