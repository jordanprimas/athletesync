from datetime import datetime
from sqlalchemy.orm import validates, foreign
from sqlalchemy import and_
from sqlalchemy_serializer import SerializerMixin

from . import db


# ------------------------------
# WellnessEntry
# ------------------------------
class WellnessEntry(db.Model, SerializerMixin):
    __tablename__ = 'wellness_entries'

    serialize_rules = (
        '-athlete',
        '-addendums.author',
        '-comments.author',
        '-likes.user'
    )

    id = db.Column(db.Integer, primary_key=True)
    athlete_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Likert-style numeric fields (1-5)
    sleep_quality = db.Column(db.Integer)
    mood = db.Column(db.Integer)
    fatigue = db.Column(db.Integer)
    soreness = db.Column(db.Integer)
    stress = db.Column(db.Integer)
    pain = db.Column(db.Integer)

    rehab_completed = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)

    # EMR-style status: active / corrected / invalid
    status = db.Column(db.String(20), default='active')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    athlete = db.relationship('User', back_populates='wellness_entries')

    # Polymorphic read-only relationships
    addendums = db.relationship(
        "Addendum",
        primaryjoin="and_(foreign(Addendum.target_id)==WellnessEntry.id, Addendum.target_type=='wellness_entry')",
        viewonly=True
    )
    likes = db.relationship(
        "Like",
        primaryjoin="and_(foreign(Like.target_id)==WellnessEntry.id, Like.target_type=='wellness_entry')",
        back_populates="wellness_entry",
        viewonly=True
    )
    comments = db.relationship(
        "Comment",
        primaryjoin="and_(foreign(Comment.target_id)==WellnessEntry.id, Comment.target_type=='wellness_entry')",
        back_populates="wellness_entry",
        viewonly=True
    )

    def __repr__(self):
        return f'<WellnessEntry id={self.id} athlete={self.athlete_id} pain={self.pain}>'
