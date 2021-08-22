from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import InputRequired, Email

# class RegisterForm(FlaskForm):
    

class UserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])


# class LoginForm(FlaskForm):
