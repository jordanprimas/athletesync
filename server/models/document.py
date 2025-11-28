from datetime import datetime
from sqlalchemy.orm import validates, foreign
from sqlalchemy import and_
from sqlalchemy_serializer import SerializerMixin

from . import db


# ------------------------------
# Document
# ------------------------------
class Document(db.Model, SerializerMixin):
    __tablename__ = 'documents'

    serialize_rules = (
        '-athlete',
        '-trainer',
        '-addendums.author'
    )

    id = db.Column(db.Integer, primary_key=True)
    athlete_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    trainer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    title = db.Column(db.String(255))
    description = db.Column(db.String(1024))
    category = db.Column(db.String(50))
    file_url = db.Column(db.String)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    athlete = db.relationship('User', foreign_keys=[athlete_id], back_populates='documents_as_athlete')
    trainer = db.relationship('User', foreign_keys=[trainer_id], back_populates='documents_as_trainer')

    addendums = db.relationship(
        "Addendum",
        primaryjoin="and_(foreign(Addendum.target_id)==Document.id, Addendum.target_type=='document')",
        viewonly=True
    )
    comments = db.relationship(
        "Comment",
        primaryjoin="and_(foreign(Comment.target_id)==Document.id, Comment.target_type=='document')",
        backref="document_parent"
    )


    def __repr__(self):
        return f'<Document id={self.id} title={self.title}>'
