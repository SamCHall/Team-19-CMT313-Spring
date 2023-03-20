from flask import render_template, request

from ..aat import app,db

from aat.models import Question,QuestionType1,QuestionType2

from .forms import CourseForm

app.config['SECRET_KEY'] = 'your secret key'

if __name__ == "__main__":
    app.run(debug=True)


@app.route("/")
def base():
    return render_template('home.html', title='Home')

@app.route("/create")
def create():
    return render_template('create.html', title='Create')

@app.route("/form", methods=["POST", "GET"])
def form():
    form = CourseForm()
    if form.validate_on_submit():
        question_text=form.title.data
        op1=form.option1.data
        op2=form.option2.data
        op3=form.option3.data
        op4=form.option4.data
        correctOption=form.correctOption.data

        qt2 = QuestionType2(question_text=question_text,option1=op1,option2=op2,option3=op3,option4=op4,question_type="question_type2",correctOption=correctOption)
        db.session.add(qt2)
        db.session.commit()

    return render_template('form.html', title='Create', form=form)


@app.route("/questions")
def questions():
    return render_template('questions.html', title='Questions')


