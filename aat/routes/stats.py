from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from .. import app, db
from ..models import Question, QuestionType1, QuestionType2

@app.route('/question/<int:id>/stats')
@login_required
def question_stats(id):
    if current_user.user_type == "staff":
        question = Question.query.filter_by(id=id).first_or_404()
        if isinstance(question, type(QuestionType1())):
            return render_template('stats/question_type1_stats.html', title=question.title, question=question)

        elif isinstance(question, type(QuestionType2())):
            abort(501)
        else:
            abort(500)

    abort(403, description="This page can only be accessed by staff.")
