from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User  # Importing the User model from the local models module
from werkzeug.security import generate_password_hash, check_password_hash
from . import db  # Importing the database object from the local module
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)  # Creating a Blueprint named 'auth'

@auth.route('/login', methods=['GET', 'POST'])
def login():
    print("Login route called")
    if request.method == 'POST':  # Check if the request method is POST
        print("Login route called with POST")
        email = request.form.get('email')  # Get the value of 'email' from the form data
        password = request.form.get('password')  # Get the value of 'password' from the form data

        user = User.query.filter_by(email=email).first()  # Query the database for a user with the provided email
        if user:  # If a user with the email is found
            if check_password_hash(user.password, password):  # Check if the provided password matches the hashed password stored in the database
                flash('Logged in successfully!', category='success')  # Display a flash message indicating successful login
                login_user(user, remember=True)  # Log in the user and remember the session
                return redirect(url_for('views.home'))  # Redirect the user to the home page
            else:  # If the password doesn't match
                flash('Incorrect password, try again.', category='error')  # Display a flash message indicating incorrect password
        else:  # If no user with the email is found
            flash('Email does not exist.', category='error')  # Display a flash message indicating that the email doesn't exist

    return render_template("login.html", user=current_user)  # Render the login template with the current user

@auth.route('/logout')
@login_required  # Ensure that the user must be logged in to access this route
def logout():
    logout_user()  # Log out the current user
    return redirect(url_for('auth.login'))  # Redirect the user to the login page


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':  # Check if the request method is POST
        print(request.form)
        email = request.form.get('email')  # Get the value of 'email' from the form data
        # name = request.form.get('name')
        password1 = request.form.get('password1')  # Get the value of 'password1' from the form data
        password2 = request.form.get('password2')  # Get the value of 'password2' from the form data

        user = User.query.filter_by(email=email).first()  # Query the database for a user with the provided email
        if user:  # If a user with the email already exists
            flash('Email already exists.', category='error')  # Display a flash message indicating that the email already exists
        elif len(email) < 4:  # If the length of the email is less than 4 characters
            flash('Email must be greater than 3 characters.', category='error')  # Display a flash message indicating that the email is too short
        # elif len(name) < 2:  # If the length of the name is less than 2 characters
        #     flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:  # If the two password fields don't match
            flash('Passwords don\'t match.', category='error')  # Display a flash message indicating that the passwords don't match
        elif len(password1) < 7:  # If the length of the password is less than 7 characters
            flash('Password must be at least 7 characters.', category='error')  # Display a flash message indicating that the password is too short
        else:  # If all the validation checks pass
            # new_user = User(email=email, first_name=name, password=generate_password_hash(
            #     password1, method='sha256'))
            new_user = User(email=email, password=generate_password_hash(
                password1, method='sha256'))  # Create a new User object with the provided email and hashed password
            db.session.add(new_user)  # Add the new user to the database session
            db.session.commit()  # Commit the changes to the database
            login_user(new_user, remember=True)  # Log in the new user and remember the session
            flash('Account created!', category='success')  # Display a flash message indicating successful account creation
            return redirect(url_for('views.home'))  # Redirect the user to the home page

    return render_template("login.html", user=current_user)  # Render the login template with the current user
