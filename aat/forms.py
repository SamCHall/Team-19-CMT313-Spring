from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired


class QuestonType1(FlaskForm):
    """Create a 'Fill in the Blank' type question."""
    title = StringField('Title')