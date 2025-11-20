from datetime import datetime
from sqlalchemy.orm import validates, foreign
from sqlalchemy import and_
from sqlalchemy_serializer import SerializerMixin

from . import db


# ------------------------------
# GroupPost
# ------------------------------
class GroupPost(db.Model, SerializerMixin):
    __tablename__ = 'group_posts'

    serialize_rules = (
        '-group',
        '-author',
        '-comments.post',
        '-likes.post',
        '-addendums.author',
    )

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)

    group = db.relationship("Group", back_populates='posts')
    author = db.relationship('User', back_populates='group_posts')

    comments = db.relationship(
        "Comment",
        primaryjoin="and_(foreign(Comment.target_id)==GroupPost.id, Comment.target_type=='post')",
        back_populates="post",
        viewonly=True
    )

    likes = db.relationship(
        "Like",
        primaryjoin="and_(foreign(Like.target_id)==GroupPost.id, Like.target_type=='post')",
        back_populates="post",
        viewonly=True
    )

    addendums = db.relationship(
        "Addendum",
        primaryjoin="and_(foreign(Addendum.target_id)==GroupPost.id, Addendum.target_type=='post')",
        viewonly=True
    )

    def __repr__(self):
        return f'<GroupPost id={self.id} group={self.group_id} author={self.author_id}>'
