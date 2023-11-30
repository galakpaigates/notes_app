from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from . import db
import re

from .models import *

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        
        data = request.form

        email = data.get("email")
        password = data.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash(message="Logged in successfully", category='success')
                user.isauthenticated = True
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash(message="Incorrect password, try again!", category='error')
        else:
            flash(message="Email does not exist!", category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    flash(message="Logged out successfully!", category='success')
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    
    if request.method == 'POST':
        data = request.form
        
        email = data.get('email')
        firstName = data.get('firstName')
        lastName = data.get('lastName')
        password1 = data.get('password1')
        password2 = data.get('password2')
        phoneNumber = data.get('phoneNumber')
        
        if User.query.filter_by(email=email).first():
            flash(message="Email already exists!", category='error')

        elif len(firstName) < 3:
            flash(message="First name must be greater than 2 characters", category='error')
            
        elif len(lastName) < 3:
            flash(message="Last name must be greater than 2 characters!", category='error')
            
        elif len(email) < 4:
            flash(message="Email must be greater than 4 characters!", category='error')
            
        elif re.match(email_regex, email) is None:
            flash(message="Invalid email address!", category='error')
        
        elif password1 != password2:
            flash(message="Passwords don't match!", category='error')
        
        elif len(password1) < 7:
            flash(message="Password must be at least 7 characters!", category='error')
        
        elif len(phoneNumber) < 7:
            flash(message="Phone number must be atleast 7 numbers!", category='error')

        elif not phoneNumber.startswith('+'):
            flash(message="Phone number must begin with '+'!", category='error')
            
        elif User.query.filter_by(phone_number=phoneNumber).first():
            flash(message="Phone number already exists!", category='error')
        
        # Add user to the database
        else:
            new_user = User(email=email, first_name=firstName, last_name=lastName, password=generate_password_hash(password1, method='pbkdf2:sha512'), phone_number=phoneNumber)
            db.session.add(new_user)
            db.session.commit()
            
            new_user.isauthenticated = True
            login_user(new_user, remember=True)
            flash(message="Account successfully created!", category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
