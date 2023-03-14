from flask import render_template
from ..models import QuestionType1

from .. import app

@app.route("/")
def home():
    
    return render_template('home.html', title='Home')

@app.route('/staff/question/create')
def create_question():
    return render_template('create-question.html')