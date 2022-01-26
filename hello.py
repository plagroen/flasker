from flask import Flask, render_template, flash, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_ckeditor import CKEditor
from datetime import date, datetime
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from webforms import UserForm, PostForm, LoginForm, NamerForm, PasswordForm, SearchForm
import uuid as uuid
import os

# Create a Flask Instance
app = Flask(__name__)
# add database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:rootpwd@localhost/flasker'
# secret key (CSRF token)
app.config['SECRET_KEY'] = "my super secret key that nobody is supposed to know"
# Upload folder
UPLOAD_FOLER = 'static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLER

# Initialize the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Flask_Login stuff
login_manager = LoginManager(app)
#login_manager.init_app(app)
login_manager.login_view = 'login'

# Rich text editor
ckeditor = CKEditor(app)

@login_manager.user_loader
def load_user(user_id):
	return Users.query.get(int(user_id))

# Pass stuff to Navbar
@app.context_processor
def base():
	form = SearchForm()
	return dict(form=form)

########### MODELS ############

# Create Blog Post Model
class Posts(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255))
	content = db.Column(db.Text)
	#author = db.Column(db.String(255))
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	date_posted = db.Column(db.DateTime, default=datetime.utcnow)
	slug = db.Column(db.String(255))

# Create Model
class Users(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), nullable=False, unique=True)
	name = db.Column(db.String(200), nullable=False)
	email = db.Column(db.String(120), nullable=False, unique=True)
	favorite_color = db.Column(db.String(120))
	date_added = db.Column(db.DateTime, default=datetime.utcnow)
	about_author = db.Column(db.Text(500), nullable=True)
	profile_picture = db.Column(db.String(72), nullable=True)
	# Do some password stuff
	password_hash = db.Column(db.String(128))
	posts = db.relationship('Posts', backref='user')

	@property
	def password(self):
		raise AttributeError('Password is not a readable attribute!')
	
	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	# Create a String
	def __repr__(self):
		return '<Name %r>' % self.name

######## ROUTES ###########

# Create a route decorator
@app.route('/')
def index():
	first_name = "John"
	stuff = "This is bold text."
	favorite_pizza = ["Pepperoni", "Cheese", "Mushrooms", 41]
	return render_template("index.html",
		first_name=first_name, 
		stuff=stuff,
		favorite_pizza=favorite_pizza)

# JSON thing
@app.route('/date')
def get_current_date():
	return {"Date": date.today()}

# Create Search function
@app.route('/search', methods=['POST'])
def search():
	form = SearchForm()
	posts = Posts.query
	if form.validate_on_submit():
		post.search_string = form.search_string.data
		posts = posts.filter(Posts.content.like('%' + post.search_string + '%'))
		posts = posts.order_by(Posts.date_posted).all()
	return render_template('search_results.html',
		form=form,
		search_string=post.search_string,
		posts=posts)

# Create Search function
@app.route('/admin')
@login_required
def admin():
	if current_user.username == 'plagroen':
		return render_template('admin.html')
	else:
		flash("The admin area is for admins only.")
		return redirect(url_for('index'))

# Create login page
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(username=form.username.data).first()
		if user:
			if user.verify_password(password=form.password.data):
				login_user(user)
				flash("You are logged in")
				return redirect(url_for('dashboard'))
			else:
				flash("Username and password don't match")
		else:
			flash("No such user.")
	return render_template('login.html', form=form)

# Create logout page
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
	logout_user()
	flash("You have been logged out. Thanks for stopping by.")
	return redirect(url_for('login'))

# Create dashboard page
@app.route('/dashboard')
@login_required
def dashboard():
	return render_template('dashboard.html')

@app.route('/posts')
def posts():
	posts = Posts.query.order_by(Posts.date_posted)
	return render_template('posts.html', posts=posts)

@app.route('/posts/<int:id>')
def post(id):
	post = Posts.query.get_or_404(id)
	return render_template('post.html', post=post)

@app.route('/add-post', methods=['GET', 'POST'])
@login_required
def add_post():
	form = PostForm()
	if form.validate_on_submit():
		user = current_user.id
		post = Posts(title=form.title.data,
			user_id=user,
			content=form.content.data,
			slug=form.slug.data)
		# Clear the form
		form.title.data = ''
		form.content.data = ''
		form.slug.data = ''
		# Save post
		db.session.add(post)
		db.session.commit()
		# Return a message
		flash("Post went succesful!")
		posts = Posts.query.order_by(Posts.date_posted)
		return render_template('posts.html', posts=posts)
	# Return a webpage
	return render_template('add_post.html', form=form)

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
	post = Posts.query.get_or_404(id)
	form = PostForm()
	user = current_user.id
	if post.user_id == user:
		if form.validate_on_submit():
			post.title = form.title.data
			post.user_id = user
			post.slug = form.slug.data
			post.content = form.content.data
			db.session.add(post)
			db.session.commit()
			flash("Post has been updated")
			return redirect(url_for('post', id=post.id))
		form.title.data = post.title
		form.slug.data = post.slug
		form.content.data = post.content
		return render_template('edit_post.html', form=form)
	else:
		flash("This post is not yours to update.")
		return redirect(url_for('post', id=post.id))

@app.route('/posts/delete/<int:id>')
@login_required
def delete_post(id):
	post_to_delete = Posts.query.get_or_404(id)
	user = current_user.id
	if post_to_delete.user_id == user:
		try:
			db.session.delete(post_to_delete)
			db.session.commit()
			flash("Post has been deleted")
		except:
			flash("Whooops! That did not go as intended. Try again.")
	else:
		flash("This post is not yours to delete.")
		return redirect(url_for('post', id=post_to_delete.id))		
	posts = Posts.query.order_by(Posts.date_posted)			
	return redirect(url_for('posts', posts=posts))

@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
	name = None
	form = UserForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(email=form.email.data).first()
		if user is None:
			#Hash password
			hashed_pwd = generate_password_hash(form.password_hash.data, "sha256")
			user = Users(username=form.username.data,
				name=form.name.data, 
				email=form.email.data, 
				favorite_color=form.favorite_color.data,
				about_author=form.about_author.data,
				password_hash=hashed_pwd)
			db.session.add(user)
			db.session.commit()
		name = form.name.data
		form.username.data = ''
		form.name.data = ''
		form.email.data = ''
		form.favorite_color.data = ''
		form.about_author.data = ''
		form.password_hash.data = ''
		flash("User " + name + " added sucessfully!")
	our_users = Users.query.order_by(Users.date_added)
	return render_template("add_user.html",
		form=form,
		name=name,
		our_users=our_users)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
	form=UserForm()
	user_to_update = Users.query.get_or_404(id)
	if request.method == 'POST':
		user_to_update.name = request.form['name']
		user_to_update.email = request.form['email']
		user_to_update.favorite_color = request.form['favorite_color']
		user_to_update.about_author = request.form['about_author']
		user_to_update.username = request.form['username']
		user_to_update.profile_picture = request.files['profile_picture']
		# Grab the filename
		pic_originalname = secure_filename(user_to_update.profile_picture.filename)
		# set UUID
		pic_finalname = str(uuid.uuid1()) + "_" + pic_originalname
		# Save that file!
		user_to_update.profile_picture.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_finalname))
		# Change the image to the name
		user_to_update.profile_picture = pic_finalname
		try:
			db.session.commit()
			flash('User updated succesfully')
		except:
			flash('Error. Looks like there was a problem. Try again...')
		return render_template("update.html",
			form=form,
			user_to_update=user_to_update)
	else:
		return render_template("update.html",
			form=form,
			user_to_update=user_to_update)

@app.route('/delete/<int:id>')
def delete(id):
	user_to_delete = Users.query.get_or_404(id)
	name = None
	form = UserForm()
	our_users = Users.query.order_by(Users.date_added)
	try:
		db.session.delete(user_to_delete)
		db.session.commit()
		flash("User deleted succesfully!")
		our_users = Users.query.order_by(Users.date_added)
	except:
		flash('Error. Looks like there was a problem. Try again...')
	return render_template("add_user.html",
		form=form,
		name=name,
		our_users=our_users)

# localhost:5000/user/john
@app.route('/user/<name>')
def user(name):
	return render_template("user.html", user_name=name)

# Create Test Password Page
@app.route('/test_pwd', methods=['GET', 'POST'])
def test_pwd():
	email = None
	password = None
	pwd_to_check = None
	passed = None
	form = PasswordForm()
	# Validate form
	if form.validate_on_submit():
		email = form.email.data
		password = form.password_hash.data
		form.email.data = '' 
		form.password_hash.data = ''
		#Lookup user
		pwd_to_check = Users.query.filter_by(email=email).first()
		#Check hashed password
		passed = pwd_to_check.verify_password(password)

	return render_template("test_pwd.html",
		email = email,
		password = password,
		pwd_to_check = pwd_to_check,
		passed = passed,
		form = form)	

# Create Name Page
@app.route('/name', methods=['GET', 'POST'])
def name():
	name = None
	form = NamerForm()
	# Validate form
	if form.validate_on_submit():
		name = form.name.data
		form.name.data = '' 
		flash("Form submitted succesfully!")

	return render_template("name.html",
		name = name,
		form = form)	


# Create Custom Error Pages

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
	return render_template("500.html"), 500
