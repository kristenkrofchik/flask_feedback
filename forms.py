from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextField
from wtforms.validators import InputRequired, Length, Email

class RegisterUserForm(FlaskForm):
    """form to add a pet to app"""
    username = StringField('Username', validators=[Length(min=4, max=20), InputRequired(message='This is a required field')])
    password = PasswordField('Password', validators=[InputRequired(message='This is a required field')])
    email = StringField('Email Address', validators=[Email(message='Please enter a valid email'), Length(min=5, max=50), InputRequired(message='This is a required field')])
    first_name = StringField('First Name', validators=[Length(min=2, max=30), InputRequired(message='This is a required field')])
    last_name = StringField('Last Name', validators=[Length(min=2, max=30), InputRequired(message='This is a required field')])

class LoginUserForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=4, max=20), InputRequired(message='This is a required field')])
    password = PasswordField('Password', validators=[InputRequired(message='This is a required field')])

class AddFeedbackForm(FlaskForm):
    title = StringField('Title', validators=[Length(min=4, max=100), InputRequired(message='This is a required field')])
    content = TextField('Feedback', validators=[InputRequired(message='This is a required field')])