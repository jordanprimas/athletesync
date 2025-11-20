from datetime import datetime
from sqlalchemy.orm import validates, foreign
from sqlalchemy import and_
from sqlalchemy_serializer import SerializerMixin

from . import db


# ------------------------------
# User-Group 
# ------------------------------

class UserGroup(db.Model):
    __tablename__ = 'user_groups'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)

    role = db.Column(db.String)

    user = db.relationship('User', back_populates='groups')
    group = db.relationship('Group', back_populates='members')

    def __repr__(self):
        return f'<UserGroup user_id={self.user_id} group_id={self.group_id}>'
