from flask_wtf import FlaskForm
from wtforms import SubmitField, widgets, StringField, BooleanField, SelectField
from wtforms.validators import DataRequired, ValidationError
from wtforms_sqlalchemy.fields import QuerySelectMultipleField, QuerySelectField
class CustomCheckboxInput(widgets.CheckboxInput):
    def __init__(self, input_id=None, *args, **kwargs):
        super(CustomCheckboxInput, self).__init__(*args, **kwargs)
        self.input_id = input_id

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', self.input_id or field.id)
        kwargs.setdefault('class', 'form-check-input')
        return super().__call__(field, **kwargs)
    
class QuerySelectMultipleFieldWithCheckboxes(QuerySelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = CustomCheckboxInput()

    def __init__(self, label='', validators=None, **kwargs):
        super(QuerySelectMultipleFieldWithCheckboxes, self).__init__(label=label, validators=validators, **kwargs)
        self.option_widget = CustomCheckboxInput(input_id='add_question_checkbox')





class CreateFormAss(FlaskForm):
    def validate_question_number_length(form, field):
        if len(form.add_question.data) != len(field.data.split(',')):
            raise ValidationError('The number of selected questions must match the number of specified question orders.')

    assignment_title = StringField(label='Assignment title:', validators=[DataRequired()])
    module_id = QuerySelectField('Select the module that can take this assignment:')
    difficulty = SelectField(label='Difficulty:', choices=[('Very Easy'), ('Easy'), ('Medium'), ('Hard'), ('Very Hard')], validators=[DataRequired()])
    add_question = QuerySelectMultipleFieldWithCheckboxes('Add questions:')
    question_order = StringField(label='Question order (comma separated):', validators=[DataRequired(), validate_question_number_length])
    is_active = BooleanField("Make assignment active?", render_kw={'class': 'form-check-input'})
    submit = SubmitField('Save')
