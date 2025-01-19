from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

check_in_questions = {
    1: {"id": 1, "question": "What is your favorite hobby?"},
    2: {"id": 2, "question": "How are you feeling today?"},
    3: {"id": 3, "question": "What is one thing you're grateful for?"},
}

custom_check_in_questions={}

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()


