from extensions.db import db


class CQModel(db.Model):
    __tablename__ = "checkin_questions"

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(80), unique=False, nullable=False)