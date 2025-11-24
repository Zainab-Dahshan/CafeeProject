from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from .. import db
from ..models.user import User
from . import auth
from .forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm, UpdateProfileForm
from ..utils.email import send_password_reset_email, send_email_confirmation

@auth.before_app_request
def before_request():
    """Update user's last seen timestamp before each request."""
    if current_user.is_authenticated:
        current_user.update_last_seen()

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        
        if user is None or not user.verify_password(form.password.data):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('auth.login'))
            
        if not user.is_active:
            flash('Your account has been deactivated.', 'warning')
            return redirect(url_for('auth.login'))
            
        login_user(user, remember=form.remember_me.data)
        
        # Redirect to the page the user was trying to access before login
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
            
        flash('You have been logged in successfully!', 'success')
        return redirect(next_page)
    
    return render_template('auth/login.html', title='Sign In', form=form)

@auth.route('/logout')
@login_required
def logout():
    """Handle user logout."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Handle new user registration."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data.lower(),
            first_name=form.first_name.data,
            last_name=form.last_name.data
        )
        user.password = form.password.data
        
        db.session.add(user)
        db.session.commit()
        
        # Send email confirmation
        send_email_confirmation(user, current_app.mail)
        flash('A confirmation email has been sent to your email address.', 'info')
        
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='Register', form=form)

@auth.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    """Handle password reset requests."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            send_password_reset_email(user, current_app.mail)
        
        flash('Check your email for instructions to reset your password', 'info')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password_request.html', title='Reset Password', form=form)

@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Handle password reset with a valid token."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    user = User.verify_reset_password_token(token)
    if not user:
        flash('Invalid or expired token', 'warning')
        return redirect(url_for('main.index'))
        
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = form.password.data
        db.session.commit()
        
        flash('Your password has been reset.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html', form=form)

@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """View and edit user profile."""
    form = UpdateProfileForm(
        original_username=current_user.username,
        original_email=current_user.email,
        username=current_user.username,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        email=current_user.email,
        phone=current_user.phone,
        address=current_user.address
    )
    
    if form.validate_on_submit():
        # Verify current password
        if not current_user.verify_password(form.current_password.data):
            flash('Current password is incorrect', 'danger')
            return redirect(url_for('auth.profile'))
        
        # Update user details
        current_user.username = form.username.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data.lower()
        current_user.phone = form.phone.data
        current_user.address = form.address.data
        
        # Update password if a new one was provided
        if form.new_password.data:
            current_user.password = form.new_password.data
        
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('auth.profile'))
    
    return render_template('auth/profile.html', title='Edit Profile', form=form)

@auth.route('/deactivate', methods=['POST'])
@login_required
def deactivate_account():
    """Deactivate the current user's account."""
    if not current_user.verify_password(request.form.get('password')):
        flash('Incorrect password', 'danger')
        return redirect(url_for('auth.profile'))
    
    # Mark user as inactive instead of deleting to preserve orders
    current_user.is_active = False
    db.session.commit()
    
    logout_user()
    flash('Your account has been deactivated. We are sorry to see you go!', 'info')
    return redirect(url_for('main.index'))
