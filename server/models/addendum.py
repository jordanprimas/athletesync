from datetime import datetime
from sqlalchemy.orm import validates, foreign
from sqlalchemy import and_
from sqlalchemy_serializer import SerializerMixin

from . import db


# ------------------------------
# Addendum (universal)
# ------------------------------
class Addendum(db.Model, SerializerMixin):
    __tablename__ = 'addendums'

    serialize_rules = (
        '-author',   
    )

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    target_type = db.Column(db.String(50), nullable=False)   # 'post' | 'wellness_entry' | 'soap_note' | 'document'
    target_id = db.Column(db.Integer, nullable=False)

    content = db.Column(db.Text, nullable=False)
    annotation_type = db.Column(db.String(20), default="revision")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    is_correction = db.Column(db.Boolean, default=False)
    is_void = db.Column(db.Boolean, default=False)

    author = db.relationship('User', back_populates='addendums')

    # convenience reverse lookups (viewonly)
    post = db.relationship(
        "GroupPost",
        primaryjoin="and_(foreign(Addendum.target_id)==GroupPost.id, Addendum.target_type=='post')",
        viewonly=True
    )
    wellness_entry = db.relationship(
        "WellnessEntry",
        primaryjoin="and_(foreign(Addendum.target_id)==WellnessEntry.id, Addendum.target_type=='wellness_entry')",
        viewonly=True
    )
    soap_note = db.relationship(
        "SOAPNote",
        primaryjoin="and_(foreign(Addendum.target_id)==SOAPNote.id, Addendum.target_type=='soap_note')",
        viewonly=True
    )
    document = db.relationship(
        "Document",
        primaryjoin="and_(foreign(Addendum.target_id)==Document.id, Addendum.target_type=='document')",
        viewonly=True
    )

    def __repr__(self):
        return f'<Addendum id={self.id} target={self.target_type}:{self.target_id} type={self.annotation_type}>'