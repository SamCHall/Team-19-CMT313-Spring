from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from ..models import QuestionType2

class QuestonType2Form(FlaskForm):
    title = StringField('Title', validators=[InputRequired(message='Please provide a title for this question'),Length(max=100)])
    option1 = StringField('Option 1',validators=[InputRequired(message='Please provide an option for this question'),Length(max=100)])
    option2 = StringField('Option 2',validators=[InputRequired(message='Please provide an option for this question'),Length(max=100)])
    option3 = StringField('Option 3',validators=[InputRequired(message='Please provide an option for this question'),Length(max=100)])
    option4 = StringField('Option 4',validators=[InputRequired(message='Please provide an option for this question'),Length(max=100)])
    correctOption = StringField('Correct Option',validators=[InputRequired()])
    Submit = SubmitField('Submit')

    # def validate_title(self, title):
    #     exists = QuestionType2.query.filter_by(title=title.data).first()
    #     if exists:
    #         raise ValidationError('A question with this title already exists')

    def validate_correctOption(self, correctOption):
        option1 = self.option1.data
        option2 = self.option2.data
        option3 = self.option3.data
        option4 = self.option4.data
        choices = [option1,option2,option3,option4]
        if correctOption.data not in choices:
            raise ValidationError('Correct Option must equal one of the options given (check capitalisation and spelling)')
        
