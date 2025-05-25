from flask_wtf import FlaskForm
from wtforms import StringField,EmailField,TextAreaField,TelField,URLField,PasswordField
from wtforms.validators import DataRequired


#form
class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    phone = TelField('Phone Number', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    subtitle = StringField('Subtitle', validators=[DataRequired()])
    img_url = URLField('Image Url', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    
class RegisterForm(FlaskForm):
     name = StringField('Name', validators=[DataRequired()])
     email = EmailField('Email', validators=[DataRequired()])
     password = PasswordField('Password', validators=[DataRequired()])
     
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    
class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired()])
    