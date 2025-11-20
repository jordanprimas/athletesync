from datetime import datetime
from sqlalchemy.orm import validates, foreign
from sqlalchemy import and_
from sqlalchemy_serializer import SerializerMixin

from . import db


# ------------------------------
# Like
# ------------------------------
class Like(db.Model, SerializerMixin):
    __tablename__ = 'likes'

    serialize_rules = (
        '-user',
        '-post',
        '-wellness_entry'
    )

    id = db.Column(db.Integer, primary_key=True)

    target_type = db.Column(db.String(50), nullable=False)   # 'post' | 'wellness_entry' | ...
    target_id = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    like_type = db.Column(db.String(20), default='like')  # 'like' | 'verify'

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='likes')

    post = db.relationship(
        "GroupPost",
        primaryjoin="and_(foreign(Like.target_id)==GroupPost.id, Like.target_type=='post')",
        back_populates="likes",
        viewonly=True
    )

    wellness_entry = db.relationship(
        "WellnessEntry",
        primaryjoin="and_(foreign(Like.target_id)==WellnessEntry.id, Like.target_type=='wellness_entry')",
        back_populates="likes",
        viewonly=True
    )

    def __repr__(self):
        return f'<Like id={self.id} user={self.user_id} target={self.target_type}:{self.target_id} type={self.like_type}>'