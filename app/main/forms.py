from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo
from ..models import User
from .validators import validator_user_already_registered

"""This is a module holding form objects"""
class CSRFDisabledForm(Form):
    # overriding init, disabling CSRF
    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(CSRFDisabledForm, self).__init__(*args, **kwargs)

# aboutMe form asking for a name from the user
class NameForm(CSRFDisabledForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    breed = StringField('What is your breed?')
    submit = SubmitField('Submit form')

class LoginForm(CSRFDisabledForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password')
    rememberMe = BooleanField('RememberMe')
    submit = SubmitField('Login')

class RegistrationForm(CSRFDisabledForm):
    email = StringField('Email', [DataRequired(), Email(), validator_user_already_registered()])
    username = StringField('Username', [Length(1,64), validator_user_already_registered()])
    password = PasswordField('Password', validators=[DataRequired(message= "Please enter a valid password!"), EqualTo('password2', message= "Passwords must match!" )])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(message= "Please confirm your password!")])
    submit = SubmitField('Register User')

class PasswordChangeForm(CSRFDisabledForm):
    old_password = StringField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('Password', validators=[DataRequired(), EqualTo('new_password2', message= "Passwords must match!" )])
    new_password2 = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Change your password')



