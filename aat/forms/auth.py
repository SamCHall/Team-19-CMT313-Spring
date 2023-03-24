from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, ValidationError

from ..models import User

def check_username(form, field):
    if User.query.filter_by(username = form.username.data).first() is None:
        raise ValidationError("Invaild Username")

def check_password(form, field):
    user = User.query.filter_by(username = form.username.data).first()
    if user:
        if not user.verify_password(password = field.data):
            raise ValidationError("Incorrect Password")

class Login_form(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired(message="Please enter a username"), check_username]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(message="Please enter a password"), check_password]
    )
    remember_me = BooleanField()
    submit = SubmitField('Log In')
