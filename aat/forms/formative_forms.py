from flask_wtf import FlaskForm
from ..aat import app
from wtforms import SubmitField, widgets, StringField, BooleanField
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectMultipleField, QuerySelectField

class QuerySelectMultipleFieldWithCheckboxes(QuerySelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class CreateFormAss(FlaskForm):
    assignment_title = StringField(label='Assignment Title:', validators=[DataRequired()])
    add_question = QuerySelectMultipleFieldWithCheckboxes('Add Questions:')
    is_active = BooleanField("Make Assessment active?")
    submit = SubmitField('Save')