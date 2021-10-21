from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class RegistrationForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired(), Length(min=3, max=15)])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=6, max=10)] )
    confirm_password = PasswordField(label='ComfirmPassword', validators=[DataRequired(), EqualTo('password')] )
    submit = SubmitField(label='Sign up', )

class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired(), Length(min=3, max=15)])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=6, max=10)] )
    submit = SubmitField(label='Sign in', )
    
class ResetRequestForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    submit = SubmitField(label='Sign in', ) 

class ResetPassworForm(FlaskForm):
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=6, max=10)] )
    confirm_password = PasswordField(label='ComfirmPassword', validators=[DataRequired(), EqualTo('password')] )
    submit = SubmitField(label='Change ´password', )           

class AccountUpdateForm(FlaskForm):
    firstname = StringField(label='Firstname', validators=[DataRequired(), Length(min=3, max=15)])
    lastname = StringField(label='Lastname', validators=[DataRequired(), Length(min=3, max=15)])
    username = StringField(label='Username', validators=[DataRequired(), Length(min=3, max=15)])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    picture=FileField(label='Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField(label='Update Account', ) 
    