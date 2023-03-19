from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from saleWA.models import Users

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                           validators = [DataRequired(), Length(2, 10)])
    email = StringField('Email',
                        validators = [DataRequired(), Email()])
    password = PasswordField('Password', 
                             validators = [DataRequired(), Length(6, 20)])
    confirm_password = PasswordField('Confirm Password',
                                     validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first() #query username, if this username exists in the data base already, it will be returned here, or else it will return none
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')
        
    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first() 
        if user:
            raise ValidationError('That email is already in use. Please use a different one.')
    
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators = [DataRequired(), Email()])
    password = PasswordField('Password', 
                             validators = [DataRequired(), Length(6, 20)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
class UpdateAccountForm(FlaskForm): #want users to be able to update their username and email for their account
    username = StringField('Username', 
                           validators = [DataRequired(), Length(2, 10)])
    email = StringField('Email',
                        validators = [DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])]) #check that the picture is an allowed file type

    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = Users.query.filter_by(username=username.data).first() #query username, if this username exists in the data base already, it will be returned here, or else it will return none
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')
        
    def validate_email(self, email):
        if email.data != current_user.email:
            user = Users.query.filter_by(email=email.data).first() 
            if user:
                raise ValidationError('That email is already in use. Please use a different one.')