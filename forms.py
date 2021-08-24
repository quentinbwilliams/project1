from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, DataRequired, Email, Length, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=1, max=25)])
    email = StringField('Email Address', validators=[Length(min=6, max=35)])
    password = PasswordField('New Password', validators=[
        DataRequired(),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    


class LoginForm(FlaskForm):
    email = StringField('Email', 
        validators=[DataRequired(),
        Email(),
        Length(min=1, max=64)])
    password = PasswordField('Password', validators=[DataRequired()])
