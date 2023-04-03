from flask_wtf import FlaskForm
from wtforms import SubmitField, widgets, StringField, BooleanField, SelectField
from wtforms.validators import DataRequired, ValidationError
from wtforms_sqlalchemy.fields import QuerySelectMultipleField, QuerySelectField

class QuerySelectMultipleFieldWithCheckboxes(QuerySelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class CreateFormAss(FlaskForm):
    def validate_question_number_length(form, field):
        if len(form.add_question.data) != len(field.data.split(',')):
            raise ValidationError('The number of selected questions must match the number of specified question orders.')

    assignment_title = StringField(label='Assignment title:', validators=[DataRequired()])
    module_id = QuerySelectField('Select the module that can take this assignment:')
    difficulty = SelectField(label='Difficulty:', choices=[('Very Easy'), ('Easy'), ('Medium'), ('Hard'), ('Very Hard')], validators=[DataRequired()])
    add_question = QuerySelectMultipleFieldWithCheckboxes('Add questions:')
    question_order = StringField(label='Question order (comma separated):', validators=[DataRequired(), validate_question_number_length])
    is_active = BooleanField("Make assignment active?")
    submit = SubmitField('Save')
