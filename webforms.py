from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea

# Create a Posts Form
class PostForm(FlaskForm):
	title = StringField("Title", validators=[DataRequired()])
	content = StringField("Content", validators=[DataRequired()], widget=TextArea())
	author = StringField("Author", validators=[DataRequired()])
	slug = StringField("Slug", validators=[DataRequired()])
	submit = SubmitField("Submit")

# Create a User Form
class UserForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired()])
	name = StringField("Name", validators=[DataRequired()])
	email = StringField("Email", validators=[DataRequired()])
	favorite_color = StringField("Favorite Color")
	password_hash = PasswordField("Password", validators=[DataRequired(), EqualTo('password_hash2', message='Passwords must match')])
	password_hash2 = PasswordField("Confirm Password", validators=[DataRequired()])
	submit = SubmitField("Submit")

# Create a Namer Form
class NamerForm(FlaskForm):
	name = StringField("What's your name", validators=[DataRequired()])
	submit = SubmitField("Submit")

# Create a Password Form
class PasswordForm(FlaskForm):
	email = StringField("What's your email", validators=[DataRequired()])
	password_hash = PasswordField("What's your password", validators=[DataRequired()])
	submit = SubmitField("Submit")

# Create a Login Form
class LoginForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired()])
	password = PasswordField("Password", validators=[DataRequired()])
	submit = SubmitField("Login")
