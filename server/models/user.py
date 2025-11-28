from datetime import datetime
from sqlalchemy.orm import validates, foreign
from sqlalchemy import and_
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash
import re

from . import db


# ------------------------------
# USER
# ------------------------------
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = (
        '-_password_hash',
        '-groups.user',
        '-soap_notes_as_athlete.user',
        '-soap_notes_as_trainer.user',
        '-wellness_entries',
        '-documents_as_athlete',
        '-documents_as_trainer',
        '-group_posts.author',
        '-comments.author',
        '-likes.user',
        '-addendums.author',
    )

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    _password_hash = db.Column(db.String)
    photo_url = db.Column(db.String, nullable=True)

    # role: 'athlete' or 'trainer'
    role = db.Column(db.String(20), nullable=False, default='athlete')

    # Relationships
    athlete_profile = db.relationship("AthleteProfile", uselist=False, back_populates="user")
    groups = db.relationship('UserGroup', back_populates='user', cascade='all, delete-orphan')
    group_posts = db.relationship('GroupPost', back_populates='author', cascade='all, delete-orphan')
    wellness_entries = db.relationship('WellnessEntry', back_populates='athlete', cascade='all, delete-orphan')
    soap_notes_as_athlete = db.relationship('SOAPNote', foreign_keys='SOAPNote.athlete_id', back_populates='athlete', cascade='all, delete-orphan')
    soap_notes_as_trainer = db.relationship('SOAPNote', foreign_keys='SOAPNote.trainer_id', back_populates='trainer', cascade='all, delete-orphan')
    documents_as_athlete = db.relationship('Document', foreign_keys='Document.athlete_id', back_populates='athlete', cascade='all, delete-orphan')
    documents_as_trainer = db.relationship('Document', foreign_keys='Document.trainer_id', back_populates='trainer', cascade='all, delete-orphan')
    comments = db.relationship('Comment', back_populates='author', cascade='all, delete-orphan')
    likes = db.relationship('Like', back_populates='user', cascade='all, delete-orphan')
    addendums = db.relationship("Addendum", back_populates="author", cascade="all, delete-orphan")

    @hybrid_property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = generate_password_hash(password)

    def authenticate(self, password):
        return check_password_hash(self._password_hash, password.encode('utf-8'))

    @validates('email')
    def validate_email(self, key, email):
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if not re.fullmatch(pattern, email):
            raise ValueError('Invalid email address')
        return email

    @validates('username')
    def validate_username(self, key, username):
        if not (3 <= len(username) <= 20):
            raise ValueError("Username must be between 3 and 20 characters")
        return username

    def __repr__(self):
        return f'<User {self.username}>'