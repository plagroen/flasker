from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField

# Create a Seach Form
class SearchForm(FlaskForm):
	search_string = StringField("Search", validators=[DataRequired()])
	submit = SubmitField("Search")

# Create a Posts Form
class PostForm(FlaskForm):
	title = StringField("Title", validators=[DataRequired()])
	#content = StringField("Content", validators=[DataRequired()], widget=TextArea())
	content = CKEditorField("Content", validators=[DataRequired()])
	slug = StringField("Slug", validators=[DataRequired()])
	submit = SubmitField("Submit")

# Create a User Form
class UserForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired()])
	name = StringField("Name", validators=[DataRequired()])
	email = StringField("Email", validators=[DataRequired()])
	favorite_color = StringField("Favorite Color")
	about_author = TextAreaField("About Author")
	password_hash = PasswordField("Password", validators=[DataRequired(), EqualTo('password_hash2', message='Passwords must match')])
	password_hash2 = PasswordField("Confirm Password", validators=[DataRequired()])
	profile_picture = FileField("Profile Picture")
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
