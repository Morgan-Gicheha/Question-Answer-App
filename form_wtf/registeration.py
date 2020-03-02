from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField
from wtforms.validators import DataRequired,InputRequired,Length,EqualTo

class Register_qa(FlaskForm):
    ''' this is a flaskform for the user registration'''
    name = StringField('name', validators=[InputRequired(), Length(max=20, message="name too long"), Length(min=4, message="name is too short")])
    email = StringField("email", validators=[InputRequired(),Length(min=12, message="seems too short for an email")])
    password = PasswordField("password",validators=[InputRequired(),Length(min=4, message="password too short!"),EqualTo("confirm_password", message="passwords don't match!") ])
    confirm_password = PasswordField("Retype password")