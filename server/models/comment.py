from datetime import datetime
from sqlalchemy.orm import validates, foreign
from sqlalchemy import and_
from sqlalchemy_serializer import SerializerMixin

from . import db


# ------------------------------
# Comment
# ------------------------------
class Comment(db.Model, SerializerMixin):
    __tablename__ = 'comments'

    serialize_rules = (
        '-author',
        '-post',
        '-wellness_entry'
    )

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

   
    target_type = db.Column(db.String(50), nullable=False)   # 'post' | 'wellness_entry' | 'soap_note' | 'document'
    target_id = db.Column(db.Integer, nullable=False)

    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    author = db.relationship('User', back_populates='comments')

 
    post = db.relationship(
        "GroupPost",
        primaryjoin="and_(foreign(Comment.target_id)==GroupPost.id, Comment.target_type=='post')",
        back_populates="comments",
        viewonly=True,
        overlaps="comments"
    )
    wellness_entry = db.relationship(
        "WellnessEntry",
        primaryjoin="and_(foreign(Comment.target_id)==WellnessEntry.id, Comment.target_type=='wellness_entry')",
        back_populates="comments",
        viewonly=True,
        overlaps="comments"
    )
    soap_note = db.relationship(
        "SOAPNote",
        primaryjoin="and_(foreign(Comment.target_id)==SOAPNote.id, Comment.target_type=='soap_note')",
        viewonly=True,
        overlaps="comments,document_parent"
    )
    document = db.relationship(
        "Document",
        primaryjoin="and_(foreign(Comment.target_id)==Document.id, Comment.target_type=='document')",
        viewonly=True,
        overlaps="comments,soap_note_parent"
    )

    @validates("target_type")
    def validate_target_type(self, key, value):
        allowed = {"post", "wellness_entry", "soap_note", "document"}
        if value not in allowed:
            raise ValueError(f"Invalid target_type '{value}'")
        return value


    def __repr__(self):
        return f'<Comment id={self.id} author={self.author_id} target={self.target_type}:{self.target_id}>'
