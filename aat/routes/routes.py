from flask import render_template, url_for, session
from flask_login import current_user, login_required
from .. import app, db
from ..models import Question, QuestionType1, FormativeAssignment, Module, Assignment, AssignQuestion, Staff, QuestionType2
from ..forms.formative_forms import CreateFormAss, AnswerFormAss
from ..forms.question_type_1 import QuestonType1Form

@app.route("/")
def home():
    return render_template('home.html', title='Home')

@login_required
@app.route("/create-formative", methods=['GET', 'POST'])
def create_assessment():
    if Staff.query.get(current_user.get_id()) != None:
        form = CreateFormAss()
        form.add_question.query = Question.query
        form.module_id.query = Module.query

        if form.validate_on_submit():
            assignment = FormativeAssignment(title = form.assignment_title.data, assignment_type = 'formative_assignment', active = form.is_active.data, module = form.module_id.data)
            db.session.add(assignment)
            db.session.commit()

            question_list = []
            for i in range(len(form.add_question.data)):
                question_list.append(form.add_question.data[i])

            question_no = 0
            for question in question_list:
                question_no += 1
                FormativeAssignment.add_question(assignment, question, question_no)
        return render_template('create_formative.html', title='Create Assessment', form = form)
    else:
        return 'Access Denied'

@app.route('/staff/question/create', methods=['GET', 'POST'])
def create_question():
    qt1_form = QuestonType1Form()
    if qt1_form.validate_on_submit():
        correct_answers = []
        for answer in qt1_form.correct_answers.data.split(','):
            correct_answers.append(answer.strip())

        incorrect_answers = []
        for answer in qt1_form.incorrect_answers.data.split(','):
            incorrect_answers.append(answer.strip())

        qt1 = QuestionType1(title=qt1_form.title.data, question_template=qt1_form.question_template.data.replace('BLANK', '{}'), correct_answers=str(correct_answers), incorrect_answers=str(incorrect_answers))
        db.session.add(qt1)
        db.session.commit()

    return render_template('create-question.html', qt1_form=qt1_form)


@app.route("/assessments", methods=['GET'])
def view_assessments():
    assignments = Assignment.query.all()
    modules = Module.query.all()
    return render_template('view_assessments_list.html', title = 'Available Assessments', assignments = assignments, modules = modules)

@app.route("/view-assessment/<int:assessment_id>", methods=['GET', 'POST'])
def answer_assessment(assessment_id):
    assignment = Assignment.query.get_or_404(assessment_id)
    questions = AssignQuestion.get_assignment_questions(assessment_id).values()
    form = AnswerFormAss()
    
    return render_template('view_assessment.html', assignment = assignment, questions = questions, title = assignment.title, form=form)
