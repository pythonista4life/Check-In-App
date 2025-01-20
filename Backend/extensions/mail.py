from flask_mail import Mail

mail = Mail()

# This function allows sending emails directly from the Flask app.
def init_mail(app):
    mail.init_app(app)