from datetime import datetime
from sqlalchemy.orm import validates, foreign
from sqlalchemy import and_
from sqlalchemy_serializer import SerializerMixin

from . import db


# ------------------------------
# SOAPNote
# ------------------------------
class SOAPNote(db.Model, SerializerMixin):
    __tablename__ = "soap_notes"

    serialize_rules = (
        '-athlete',
        '-trainer',
    )

    id = db.Column(db.Integer, primary_key=True)
    athlete_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    trainer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    subjective = db.Column(db.Text)
    objective = db.Column(db.Text)
    assessment = db.Column(db.Text)
    plan = db.Column(db.Text)

    injury_location = db.Column(db.String)
    injury_type = db.Column(db.String)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    athlete = db.relationship('User', foreign_keys=[athlete_id], back_populates='soap_notes_as_athlete')
    trainer = db.relationship('User', foreign_keys=[trainer_id], back_populates='soap_notes_as_trainer')

    # Addendums (read-only polymorphic)
    addendums = db.relationship(
        "Addendum",
        primaryjoin="and_(foreign(Addendum.target_id)==SOAPNote.id, Addendum.target_type=='soap_note')",
        viewonly=True
    )

    def __repr__(self):
        return f'<SOAPNote id={self.id} athlete={self.athlete_id} trainer={self.trainer_id}>'
