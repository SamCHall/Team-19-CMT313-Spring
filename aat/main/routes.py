from flask import render_template, url_for
from ..models import QuestionType1
from ..forms import QuestonType1Form
from .. import app, db


@app.route("/")
def home():
    
    return render_template('home.html', title='Home')

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