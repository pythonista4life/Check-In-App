from extensions.db import db


class CQModel(db.Model):

    # The name of the database table.
    __tablename__ = "checkin_questions"

    # Database columns.
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(80), unique=False, nullable=False)
