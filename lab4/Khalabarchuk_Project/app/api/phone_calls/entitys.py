from datetime import datetime

from app import db


class PhoneCall(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_caller = db.Column(db.String(12), unique=False, nullable=False)
    second_caller = db.Column(db.String(12), unique=False, nullable=False)
    start_time = db.Column(db.DateTime, nullable=True, default=datetime.now().replace(microsecond=0))
    end_time = db.Column(db.DateTime, nullable=True, default=datetime.now().replace(microsecond=0))
