from flask import render_template, request

from ..aat import app,db

from aat.models import Question,QuestionType1

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

@app.route("/form", methods=('GET', 'POST'))
def form():
    form = CourseForm()
    return render_template('form.html', title='Create', form=form)


@app.route("/questions")
def questions():
    return render_template('questions.html', title='Questions')

# methods=["POST","GET"]
@app.route("/addquestion", methods=["POST", "GET"])
def add_question():

    ques=request.form.get('question')
    op1=request.form.get('op1')
    op2=request.form.get('op2')
    op3=request.form.get('op3')
    op4=request.form.get('op4')
    correctOption=request.form.get('correctOption')


    Question = QuestionType1(question_text=ques,option1=op1,option2=op2,option3=op3,option4=op4,question_type="question_type1",correctOption=correctOption)
    db.session.add(Question)
    db.session.commit()
    
    return render_template("home.html")
