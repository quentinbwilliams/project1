from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    email = StringField('Email', 
        validators=[DataRequired(),
        Email(),
        Length(min=1, max=64)])
    password = PasswordField('Password', validators=[DataRequired()])