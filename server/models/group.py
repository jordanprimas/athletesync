from datetime import datetime
from sqlalchemy.orm import validates, foreign
from sqlalchemy import and_
from sqlalchemy_serializer import SerializerMixin

from . import db


# ------------------------------
# Group 
# ------------------------------
class Group(db.Model, SerializerMixin):
    __tablename__ = 'groups'

    serialize_rules = (
        '-members.group',
        '-posts.group'
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(255))
    cover_image = db.Column(db.String(255))

    members = db.relationship('UserGroup', back_populates='group', cascade='all, delete-orphan')
    posts = db.relationship('GroupPost', back_populates='group', cascade='all, delete-orphan')

    @validates('name')
    def validate_name(self, key, name):
        if not (3 <= len(name) <= 50 ):
            raise ValueError('Group name must be between 3 and 50 characters')
        return name

    def __repr__(self):
        return f'<Group: {self.name}>'


