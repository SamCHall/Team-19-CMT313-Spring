from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, ValidationError


class QuestonType1Form(FlaskForm):
    """Create a 'Fill in the Blank' type question."""
    title = StringField('Title', validators=[InputRequired(message='Please provide a title for this question.')])
    question_template = StringField('Provide a question template using "{}" to place blanks', validators=[InputRequired(message='Please provide a sentence with blanks {} to be filled in.')])
    correct_answers = StringField('Correct answers', validators=[InputRequired('Please provide the correct answers.')])
    incorrect_answers = StringField('Incorrect answers')
    submit = SubmitField('Confirm')

    def validate_question_text(self, question_template):
        if "{}" not in question_template:
            raise ValidationError('Your template must include at least one blank which is done by placing curly braces, {}, in place of a word.')

