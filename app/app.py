# Note: it is important to add "render_template" to the imports
from flask import Flask, render_template, request
from flask import redirect, url_for, flash, abort

# Flask-Login is a Flask extension that provides a framework for handling user authentication
import flask_login
from flask_login import LoginManager
from flask_login import login_required
# Logs a user in. We should pass the actual user object to this method:
# returns True if the log in attempt succeeds, and False if it fails
from flask_login import login_user

# Security and Forms for the login
import werkzeug.security as ws
# from forms import LoginForm

# Import the Image module from the PIL (Python Imaging Library) package. 
# Used to preprocess the images uploaded by the users. 
# Ensure 'Pillow' is installed before running the application by using
# the command 'pip install Pillow'
from PIL import Image
PROFILE_IMG_HEIGHT = 130
POST_IMG_WIDTH = 300

# Import the datetime library to handle the pubblication dates of the posts or insertions
# import datetime

## Import the dao modules and the models module
import models
import users_dao

## Here I call these functions for the creation of the DB tables at startup time
from table_creation import create_table_users
create_table_users()

# create the application
app = Flask(__name__)

app.config['SECRET_KEY'] = 'gematria'

# This is for login_manager 
login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/')
def home():
    return render_template('home.html', title='Home', active_page='home')

#########################################################
#########################################################
#########################################################
#######First the login and the sign-up page##############
#########################################################
#########################################################
#########################################################
#########################################################

# Define the signup page
@app.route('/signup')
def signup():
    return render_template('signup.html', active_page="signup")

@app.route('/signup', methods=['GET', 'POST'])
def signup_function():

    # I take from the form the input datas and import them locally as a dictionary
    new_user_form = request.form.to_dict()

    # I try to retrieve the unique email of the nuovo_utente_form from the db ..
    user_in_db = users_dao.get_user_by_email(new_user_form.get('email'))

    # ... and I check weather it has already been registered ..
    if user_in_db:
        flash('There\'s already a user with these credentials', 'danger')
        return redirect(url_for('signup'))
    # .. and if it hasn't been registered ..
    else:
        # I generate an hash for the password that has been inserted by the form input
        new_user_form['password'] = ws.generate_password_hash(new_user_form.get('password'))

        # I add the user to the db using the method "add_user" from the utenti_dao.py
        success = users_dao.add_user(new_user_form)

        if success:
            flash('Utente creato correttamente', 'success')
            return redirect(url_for('home'))
        else:
            flash('Errore nella creazione del utente: riprova!', 'danger')
            return redirect(url_for('signup'))

@login_manager.user_loader
def load_user(user_id):
    db_user = users_dao.get_user_by_id(user_id)
    if db_user is not None:
        user = models.User(id=db_user['id'], 
                           email=db_user['email'],
                           password=db_user['password'])
    else:
        user = None
    return user

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html', active_page="login")

@app.route('/login', methods=['POST'])
def login_post():

    # Retrieving the informations from the form @ /login
    user_form = request.form.to_dict()
    # Using the "get_user_by_nickname" method from utenti.dao, which
    # retrieves the user from the database with the given nickname passed
    # from the form in /login
    utente_db = users_dao.get_user_by_email(user_form['email'])

    # If there's no utente_db in the database (meaning the user just doesn't exist into the db)
    # or if the password given as input in the form /login isn't equal to the one in the database
    if not utente_db or not ws.check_password_hash(utente_db['password'], user_form['password']):
        flash('Invalid credentials, retry', 'danger')
        return redirect(url_for('home'))
    else:
    # if, instead, it exists, we create a new user instance using the "User model" defined in models.py
        # Create a new user instance called "new"
        new = models.User(id=utente_db['id'], 
                          email=utente_db['email'],
                          password=utente_db['password'])
        # We log in said user called "new"
        flask_login.login_user(new, True)
        flash('Welcome back ' + utente_db['email'] + '!', 'success')
        return redirect(url_for('home'))

# Log out route
@app.route("/logout")
@login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for('home'))

@app.route('/about')
def about():
    return render_template('about.html', title='About Us', active_page='about')
