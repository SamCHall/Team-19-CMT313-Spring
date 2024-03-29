from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import InputRequired, ValidationError
from ..models import Question


class QuestionType1FormCreate(FlaskForm):
    """Create a 'Fill in the Blank' type question."""
    title = StringField('Title', validators=[InputRequired(message='Please provide a title for this question.')])
    question_template = StringField('Provide a question template including "BLANK" where appropriate.', validators=[InputRequired(message='Please provide a sentence with blanks {} to be filled in.')])
    correct_answers = StringField('Comma separated list of correct answers.', validators=[InputRequired('Please provide the correct answers.')])
    incorrect_answers = StringField('Comma separated list of incorrect answers (optional).')
    difficulty = SelectField('Difficulty', choices=['', 'Very Easy', 'Easy', 'Medium', 'Hard', 'Very Hard'])
    submit = SubmitField('Confirm')

    def validate_title(self, title):
        exists = Question.query.filter_by(title=title.data).first()
        if exists:
            raise ValidationError('A question with this title already exists')

    def validate_question_template(self, question_template):
        if "BLANK" not in question_template.data:
            raise ValidationError('Your template must include at least one BLANK')

    def validate_correct_answers(self, correct_answers):
        n_of_blanks = self.question_template.data.count('BLANK')
        if not len(correct_answers.data.split(',')) == n_of_blanks:
            raise ValidationError('Number of correct answers must match the number of "BLANK"s in the template.')
        

class QuestionType1FormEdit(FlaskForm):
    """Edit a 'Fill in the Blank' type question."""
    title = StringField('Title', validators=[InputRequired(message='Please provide a title for this question.')])
    question_template = StringField('Provide a question template including "BLANK" where appropriate.', validators=[InputRequired(message='Please provide a sentence with blanks {} to be filled in.')])
    correct_answers = StringField('Comma separated list of correct answers.', validators=[InputRequired('Please provide the correct answers.')])
    incorrect_answers = StringField('Comma separated list of incorrect answers (optional).')
    difficulty = SelectField('Difficulty', choices=['', 'Very Easy', 'Easy', 'Medium', 'Hard', 'Very Hard'])
    submit = SubmitField('Confirm')

    def validate_question_template(self, question_template):
        if "BLANK" not in question_template.data:
            raise ValidationError('Your template must include at least one BLANK')

    def validate_correct_answers(self, correct_answers):
        n_of_blanks = self.question_template.data.count('BLANK')
        if not len(correct_answers.data.split(',')) == n_of_blanks:
            raise ValidationError('Number of correct answers must match the number of "BLANK"s in the template.')
