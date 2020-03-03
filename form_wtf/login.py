from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField
from wtforms.validators import InputRequired

class Login(FlaskForm):
    '''this is a wtfbased class for the login page'''
    name = StringField("name",validators=[InputRequired(message="name is required for login")])
    password = PasswordField("password",validators=[InputRequired(message="enter password")])