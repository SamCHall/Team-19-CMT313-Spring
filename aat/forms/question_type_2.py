from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Length

class QuestonType2Form(FlaskForm):
    title = StringField('Title', validators=[InputRequired(),Length(max=100)])
    option1 = StringField('Option 1',validators=[InputRequired(),Length(max=100)])
    option2 = StringField('Option 2',validators=[InputRequired(),Length(max=100)])
    option3 = StringField('Option 3',validators=[InputRequired(),Length(max=100)])
    option4 = StringField('Option 4',validators=[InputRequired(),Length(max=100)])
    correctOption = StringField('Correct Option',validators=[InputRequired(),Length(max=100)])
    Submit = SubmitField('Submit')
