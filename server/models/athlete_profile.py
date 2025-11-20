from datetime import datetime
from sqlalchemy.orm import validates, foreign
from sqlalchemy import and_
from sqlalchemy_serializer import SerializerMixin

from . import db


# ------------------------------
# AthleteProfile
# ------------------------------
class AthleteProfile(db.Model, SerializerMixin):
    __tablename__ = "athlete_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)

    sport = db.Column(db.String)
    position = db.Column(db.String)
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    dob = db.Column(db.Date)
    injury_history = db.Column(db.Text)

    user = db.relationship('User', back_populates='athlete_profile')

    def __repr__(self):
        return f'<AthleteProfile user_id={self.user_id}>'