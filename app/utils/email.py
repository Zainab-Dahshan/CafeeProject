"""
Email utility functions for the Café application.
"""
from flask import current_app, render_template
from flask_mail import Message

def send_email(subject, sender, recipients, text_body, html_body, mail_instance=None):
    """Send an email.
    
    Args:
        subject (str): The email subject.
        sender (str): The email sender address.
        recipients (list): List of recipient email addresses.
        text_body (str): Plain text email body.
        html_body (str): HTML email body.
        mail_instance: The Flask-Mail instance.
    """
    from flask_mail import Message
    msg = Message(
        subject=subject,
        sender=sender,
        recipients=recipients,
        body=text_body,
        html=html_body
    )
    mail_instance.send(msg)

def send_password_reset_email(user, mail_instance):
    """Send a password reset email to the user.
    
    Args:
        user (User): The user who requested a password reset.
        mail_instance: The Flask-Mail instance.
    """
    token = user.get_reset_password_token()
    send_email(
        subject='[Café] Reset Your Password',
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipients=[user.email],
        text_body=render_template('email/reset_password.txt', user=user, token=token),
        html_body=render_template('email/reset_password.html', user=user, token=token),
        mail_instance=mail_instance
    )

def send_email_confirmation(user, mail_instance):
    """Send an email confirmation email to the user.
    
    Args:
        user (User): The user who registered.
        mail_instance: The Flask-Mail instance.
    """
    token = user.generate_confirmation_token()
    send_email(
        subject='[Café] Confirm Your Email',
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipients=[user.email],
        text_body=render_template('email/confirm_email.txt', user=user, token=token),
        html_body=render_template('email/confirm_email.html', user=user, token=token)
    )
