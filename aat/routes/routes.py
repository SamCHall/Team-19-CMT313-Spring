import random
import ast
from flask import render_template, abort, flash, request, redirect, url_for
from flask_login import current_user, login_required

from .. import app, db
from ..models import *
from ..forms.formative_forms import CreateFormAss
from ..forms.question_type_1 import QuestionType1FormCreate, QuestionType1FormEdit
from ..forms.question_type_2 import QuestionType2FormCreate, QuestionType2FormEdit



# Home
@app.route("/")
def home():
    return render_template('home.html', title='Home')



@app.route("/staff/create-formative", methods=['GET', 'POST'])
@login_required
def create_formative_assessment():
    if Staff.query.get(current_user.get_id()) == None:
        abort(403, description="This page can only be accessed by staff.")
    form = CreateFormAss()
    form.add_question.query = Question.query.filter_by(archived=False)
    form.module_id.query = Module.query

    if form.validate_on_submit():
        assignment = FormativeAssignment(title = form.assignment_title.data,
                                         assignment_type = 'formative_assignment',
                                         active = form.is_active.data,
                                         module = form.module_id.data,
                                         difficulty = form.difficulty.data
                                         )
        db.session.add(assignment)
        db.session.commit()

        flash("You've created a new formative assessment!")

        question_list = []
        for i in range(len(form.add_question.data)):
            question_list.append(form.add_question.data[i])

        question_order = [int(q) for q in form.question_order.data.split(',')]

        for question in question_list:
            FormativeAssignment.add_question(assignment, question, question_order.pop(0))

    return render_template('create_formative.html', title='Create Assessment', form = form, error=form.errors.get('question_order'))



# Create a summative assessment
@app.route('/create-summative', methods=['GET', 'POST'])
@login_required
def create_summative_assessment():
    return render_template('create_summative.html')



# Create a type 1 question
@app.route('/staff/question/create/type1', methods=['GET', 'POST'])
@login_required
def create_question_type1():
    qt1_form = QuestionType1FormCreate()
    if qt1_form.validate_on_submit():
        correct_answers = []
        for answer in qt1_form.correct_answers.data.split(','):
            correct_answers.append(answer.strip())

        incorrect_answers = []
        for answer in qt1_form.incorrect_answers.data.split(','):
            incorrect_answers.append(answer.strip())

        qt1 = QuestionType1(
            title=qt1_form.title.data,
            question_template=qt1_form.question_template.data.replace('BLANK', '{}'),
            correct_answers=str(correct_answers),
            incorrect_answers=str(incorrect_answers),
            difficulty=qt1_form.difficulty.data
        )

        db.session.add(qt1)
        db.session.commit()

        flash("You've created a new Fill in the Blank question!")
        return redirect(url_for('questions'))

    return render_template('create-question-type1.html', qt1_form=qt1_form)



# Create a type 2 question
@app.route("/staff/question/create/type2", methods=["POST", "GET"])
@login_required
def create_question_type2():
    form = QuestionType2FormCreate()
    if form.validate_on_submit():
        question_text=form.title.data
        op1=form.option1.data
        op2=form.option2.data
        op3=form.option3.data
        op4=form.option4.data
        correctOption=form.correctOption.data

        qt2 = QuestionType2(
            question_text=question_text,
            title=question_text,
            option1=op1,
            option2=op2,
            option3=op3,
            option4=op4,
            question_type="question_type2",
            correctOption=correctOption
        )

        db.session.add(qt2)
        db.session.commit()
        flash("You've created a new Multiple Choice question!")
        return redirect(url_for('questions'))

    return render_template('create-question-type2.html', title='Create', form=form)



@app.route("/display-questions", methods=['GET','POST'])
def questions():
    active_questions = Question.query.filter_by(archived=False).all()
    archived_questions = Question.query.filter_by(archived=True).all()
    return render_template('display-questions.html', title='Questions', questions=active_questions, archived=archived_questions)



@app.route("/assessments", methods=['GET'])
def view_assessments():
    assignments = Assignment.query.all()
    for assignment in assignments:
        assignment.mark = assignment.get_student_highest_mark(current_user.id)
        assignment.total_mark = assignment.total_available_mark()
    return render_template('view_assessments_list.html', title = 'Available Assessments', assignments = assignments)



@app.route("/staff/assessments", methods=['GET'])
@login_required
def view_staff_assessments():
    if Staff.query.get(current_user.get_id()) == None:
        abort(403, description="This page can only be accessed by staff.")
    assignments = Assignment.query.all()
    return render_template('view_assessments_list_staff.html', title = 'Assessments - Staff View', assignments = assignments)



@app.route("/view-assessment/<int:assessment_id>", methods=['GET', 'POST'])
@login_required
def view_assessment(assessment_id):
    assignment = Assignment.query.get_or_404(assessment_id)
    questions = AssignQuestion.get_assignment_questions(assessment_id).values()

    for question in questions:
        if question.question_type == "question_type1":

            # Replaces {} in the template with a dropzone
            question.question_template = str(question.question_template).replace("{}","<span class=\"dropzone\" id=\"question{{loop.index}}\"></span>")

            # Takes the string literal and converts it to a list of strings
            a = ast.literal_eval(question.correct_answers)
            b = ast.literal_eval(question.incorrect_answers)
            # Making both lists into one
            c = a + b

            # Randomises the order of options from correct_answers and incorrect_answers
            question.options = random.sample(c, len(c))

    if current_user.user_type == "student":
        if assignment.active == False:
            abort(403, description="This assignment is currently not active. Please wait for staff to make it available")

        if not assignment.module.check_student(current_user):
            abort(403, description="You are not enrolled on the correct module to take this assignment.")

        return render_template('view_assessment.html', assignment = assignment, questions = questions, title = assignment.title)

    elif current_user.user_type == "staff":
        if not assignment.module.check_staff(current_user):
            abort(403, description="You are not a staff member on this module.")

        return render_template('view_assessment_read_only.html', assignment = assignment, questions = questions, title = assignment.title)



@app.route('/submit-assessment/<int:assessment_id>', methods=['GET','POST'])
@login_required
def submit_assessment(assessment_id):

    assignment = Assignment.query.get_or_404(assessment_id)
    questions = AssignQuestion.get_assignment_questions(assessment_id).values()

    if assignment.active == False:
        abort(403, description="This assignment is currently not active. Please wait for staff to make it available")

    if not assignment.module.check_student(current_user):
        abort(403, description="You are not enrolled on the correct module to take this assignment.")

    type1_answer_values = request.get_json()['optionValues']
    type2_answer_values = request.get_json()['type2Values']

    type2_questions = [] # Needed for marking individual questions in later step

    type1_correct_answers_list = []
    type2_correct_answers_list = []

    for question in questions:
        if question.question_type == 'question_type1':
            correct_answers = ast.literal_eval(question.correct_answers)

            for correct_answer in correct_answers:
                type1_correct_answers_list.append(correct_answer)

        elif question.question_type == 'question_type2':
            type2_questions.append(question)
            type2_correct_answers_list.append(question.correctOption)

    # The below code is used to mark the overall assessment before adding a submission to the database
    type1_mark = 0
    for answer in range(len(type1_answer_values)):
        if type1_answer_values[answer] == type1_correct_answers_list[answer]:
            type1_mark += 1

    type2_mark = 0
    for answer in range(len(type2_answer_values)):
        if type2_answer_values[answer] == type2_correct_answers_list[answer]:
            type2_mark += 1

    total_answer_mark = type1_mark + type2_mark
    total_available_mark = len(type1_correct_answers_list) + len(type2_correct_answers_list)
    current_attempt_number = Submission.get_current_attempt_number(current_user.id, assessment_id)

    submission = Submission(
            assignment_id = assignment.id,
            student_id = current_user.id,
            mark = total_answer_mark,
            attempt_number = current_attempt_number + 1
            )

    simplified_submission = SimplifiedSubmission(
            assignment_title = assignment.title,
            student_id = current_user.id,
            total_mark = total_answer_mark,
            total_available_mark = total_available_mark,
            module_id = assignment.module.id
    )
    db.session.add(simplified_submission)

    # The below code is used to add the answers to the database with their individual marks.
    for question in questions:
        if question.question_type == 'question_type1':
            num_blanks = QuestionType1.num_of_blanks(question)
            submitted_answer = []
            mark = 0
            for i in range(num_blanks):
                submitted_answer.append(type1_answer_values[i])
                if submitted_answer[i] == type1_correct_answers_list[i]:
                    mark += 1
            submission.add_question_answer(question, str(submitted_answer), mark)
            type1_answer_values = type1_answer_values[num_blanks:] # Trims off the start of the list so the for loop begins again at the next question.
        else:

            submitted_answer = type2_answer_values[type2_questions.index(question)] # Gets the index of the question in the list of questions and uses that to get the answer from the list of answers.

            if question.correctOption == submitted_answer:
                submission.add_question_answer(question, submitted_answer, 1)
            else:
                submission.add_question_answer(question, submitted_answer, 0)


    # This will need to redirect to a page that shows the results of the assessment eventually.
    return redirect(request.referrer)



@app.route('/questions/delete/<int:id>')
def delete_question(id):
    question_to_delete = Question.query.get_or_404(id)
    if bool(question_to_delete.active):
        flash("Question is active so it can't be deleted.")
        return render_template('display-questions.html', title='Questions',questions=questions)
    else:
        try:
            db.session.delete(question_to_delete)
            db.session.commit()

            flash("Question was deleted")
        
            questions = Question.query.all()
            return render_template('display-questions.html', title='Questions',questions=questions)
        
        except Exception as e:
            print(e)
            flash("There was a problem deleting the question")
            return redirect('/')



@app.route('/questions/edit/<int:id>', methods=['GET','POST'])
def edit_question(id):
    question = Question.query.get_or_404(id)

    if question.question_type == 'question_type1':
        qt1_form = QuestionType1FormEdit()

        if qt1_form.validate_on_submit():
            correct_answers = []
            for answer in qt1_form.correct_answers.data.split(','):
                correct_answers.append(answer.strip())

            incorrect_answers = []
            for answer in qt1_form.incorrect_answers.data.split(','):
                incorrect_answers.append(answer.strip())
            
            question.title = qt1_form.title.data
            question.question_template = qt1_form.question_template.data.replace('BLANK', '{}')
            question.correct_answers = str(correct_answers)
            question.incorrect_answers = str(incorrect_answers)
            question.difficulty = qt1_form.difficulty.data
            flash("Question successfully updated")
            db.session.commit()
            return redirect(url_for('questions', id=question.id))

        qt1_form.title.data = question.title
        qt1_form.question_template.data = question.question_template.replace('{}', 'BLANK')
        qt1_form.correct_answers.data = ', '.join(ast.literal_eval(question.correct_answers))
        qt1_form.incorrect_answers.data = ', '.join(ast.literal_eval(question.incorrect_answers))
        qt1_form.difficulty.data = question.difficulty
        return render_template('edit-qt1.html', qt1_form=qt1_form)
    
    else:
        form = QuestionType2FormEdit()
        if form.validate_on_submit():
            question.title = form.title.data
            question.option1 = form.option1.data
            question.option2 = form.option2.data
            question.option3 = form.option3.data
            question.option4 = form.option4.data
            question.correctOption = form.correctOption.data

            # db.session.add(question)
            db.session.commit()
            flash("Question successfully updated")
            return redirect(url_for('questions',id=question.id))
        
        form.title.data = question.title
        form.option1.data = question.option1
        form.option2.data = question.option2
        form.option3.data = question.option3
        form.option4.data = question.option4
        form.correctOption.data = question.correctOption

        return render_template('edit-qt2.html', form = form)



@app.route('/display-questions/<int:id>')
def view_question(id):
    question = Question.query.get_or_404(id)
    if question.question_type == 'question_type1':
        correct_answers = ast.literal_eval(question.correct_answers)
        incorrect_answers = ast.literal_eval(question.incorrect_answers)
        all_answers = correct_answers + incorrect_answers
        random.shuffle(all_answers)

        question.complete = question.question_template.format(*correct_answers)
        return render_template('view-question-type1.html', question=question, all_answers=all_answers)
    else:
        return render_template('view-question-type2.html', question=question)



@app.route("/students")
@login_required
def student_list():
    students = Student.query.all()

    return render_template('student_list.html', title="Students", students=students)



@app.route('/staff/edit-formative/<int:assessment_id>', methods=['GET', 'POST'])
@login_required
def edit_formative_assessment(assessment_id):
    assignment = FormativeAssignment.query.get(assessment_id)

    if Staff.query.get(current_user.get_id()) == None:
        abort(403, description="This page can only be accessed by staff.")

    if not assignment.module.check_staff(current_user):
            abort(403, description="You are not a staff member on this module.")

    form = CreateFormAss()
    form.add_question.query = Question.query
    form.module_id.query = Module.query
    questions = AssignQuestion.get_assignment_questions(assessment_id) # Get the questions in the assignment

    if form.validate_on_submit():
        assignment.title = form.assignment_title.data
        assignment.active = form.is_active.data
        assignment.module = form.module_id.data
        assignment.difficulty = form.difficulty.data

        question_list = []
        for i in range(len(form.add_question.data)):
            question_list.append(form.add_question.data[i])

        question_order = [int(q) for q in form.question_order.data.split(',')] # Split the string into a list of integers

        for question in questions.values():
                    if question not in question_list:
                        AssignQuestion.query.filter_by(assignment_id=assessment_id, question_id=question.id).delete() # Delete the question from the assignment if it's not in the list of questions

        for question in question_list:
            question_query = AssignQuestion.query.filter_by(assignment_id=assessment_id, question_id=question.id) # Get the question from the assignment
            if question_query.first() is not None: # If the question is already in the assignment
                question_query.update({'question_number': question_order.pop(0)}) # Update the question number
            else:
                FormativeAssignment.add_question(assignment, question, question_order.pop(0)) # Add the question to the assignment

        db.session.commit()

        flash("You've edited a formative assessment!")
        return redirect(url_for('view_staff_assessments')) # Redirect to the staff assessments page




    form.assignment_title.data = assignment.title
    form.is_active.data = assignment.active
    form.module_id.data = assignment.module
    form.difficulty.data = assignment.difficulty

    if AssignQuestion.query.filter_by(assignment_id=assessment_id).first() is not None: # If there are questions in the assignment
        assignment.questions = questions
        form.add_question.data = [q for q in assignment.questions.values()] # Set the questions in the assignment to the form
        current_question_order = ""
        for question in Question.query:
            if question in assignment.questions.values():
                current_question_order += str(list(assignment.questions.values()).index(question) + 1) + "," # Add the question order to the string
        current_question_order = current_question_order[:-1] # Remove the last comma
        form.question_order.data = current_question_order # Set the question order to the form

    return render_template('edit_formative.html', title='Edit Assessment', form = form, assignment = assignment, error=form.errors.get('question_order'))



@app.route('/delete-assessment/<int:assessment_id>', methods=['GET', 'POST'])
@login_required
def delete_assessment(assessment_id):
    assignment = Assignment.query.get_or_404(assessment_id)

    if Staff.query.get(current_user.get_id()) == None:
        abort(403, description="This page can only be accessed by staff.")

    if current_user not in assignment.module.get_staff():
        abort(403, description="You are not a staff member for this module.")

    questions = list(Assignment.get_questions(assignment).values())
    question_ids = []
    for question in questions:
        question_ids.append(question.id)

    db.session.delete(assignment)

    for question_id in question_ids:
        if AssignQuestion.query.filter_by(question_id=question_id).first() is None:
            Question.query.filter_by(id=question_id).update({"active": False})

    db.session.commit()

    flash('The assessment has been deleted successfully.')
    return redirect(request.referrer)



@app.route('/archive-assessment/<int:assessment_id>', methods=['GET', 'POST'])
@login_required
def archive_assessment(assessment_id):
    assignment = Assignment.query.get_or_404(assessment_id)

    if Staff.query.get(current_user.get_id()) == None:
        abort(403, description="This page can only be accessed by staff.")

    if current_user not in assignment.module.get_staff():
        abort(403, description="You are not a staff member for this module.")

    assignment.active = False
    db.session.commit()
    flash('The assessment has been archived successfully.')

    return redirect(request.referrer)



@app.route('/unarchive-assessment/<int:assessment_id>', methods=['GET', 'POST'])
@login_required
def unarchive_assessment(assessment_id):
    assignment = Assignment.query.get_or_404(assessment_id)

    if Staff.query.get(current_user.get_id()) == None:
        abort(403, description="This page can only be accessed by staff.")

    if current_user not in assignment.module.get_staff():
        abort(403, description="You are not a staff member for this module.")

    assignment.active = True
    db.session.commit()
    flash('The assessment has been activated successfully.')
    return redirect(request.referrer)



@app.route('/archive-question/<int:id>')
@login_required
def archive_question(id):
    question = Question.query.get_or_404(id)

    if bool(question.active):
        flash("Question is active so it can't be archived.")
        return redirect(request.referrer)
    else:
        question.archived = not question.archived
        db.session.commit()
        if question.archived:
            flash(f'{question.title} has been archived.')
        else:
            flash(f'{question.title} has been re-activated.')
        return redirect(request.referrer)
