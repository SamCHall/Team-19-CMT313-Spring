from flask_wtf import FlaskForm
from wtforms import SubmitField, widgets, StringField, BooleanField, RadioField
from ..models import Question
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectMultipleField, QuerySelectField, QueryRadioField

class QuerySelectMultipleFieldWithCheckboxes(QuerySelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class CreateFormAss(FlaskForm):
    assignment_title = StringField(label='Assignment title:', validators=[DataRequired()])
    module_id = QuerySelectField('Select the module that can take this assignment:')
    add_question = QuerySelectMultipleFieldWithCheckboxes('Add questions:')
    is_active = BooleanField("Make assignment active?")
    submit = SubmitField('Save')

class AnswerFormAss(FlaskForm):
    
    submit = SubmitField('Submit Answer')
