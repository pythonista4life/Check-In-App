from extensions.db import db


class CCQModel(db.Model):

    # The name of the database table.
    __tablename__ = "custom_checkin_questions"

    # Database columns.
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(80), unique=False, nullable=False)
    user_id = db.Column(db.Integer, unique=False, nullable=False)
