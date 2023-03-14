from flask import render_template

from ..aat import app, db
from aat.models import Question, FormativeAssignment, Module, Assignment, AssignQuestion
from aat.forms.formative_forms import CreateFormAss

@app.route("/")
def home():
    return render_template('home.html', title='Home')

@app.route("/create", methods=['GET', 'POST'])
def create_assessment():
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

@app.route("/assessments", methods=['GET'])
def view_assessments():
    assignments = Assignment.query.all()
    modules = Module.query.all()
    return render_template('view_assessments_list.html', title = 'Available Assessments', assignments = assignments, modules = modules)

@app.route("/view-assessment/<int:assessment_id>")
def view_assessment(assessment_id):
    assignment = Assignment.query.get_or_404(assessment_id)
    questions = AssignQuestion.get_assignment_questions(assessment_id).values()
    
    return render_template('view_assessment.html', assignment = assignment, questions = questions, title = assignment.title)