from sqlalchemy import and_
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates, foreign
from datetime import datetime
import re

# Local imports 
from config import db, bcrypt, generate_password_hash, check_password_hash


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
        password_hash = generate_password_hash(password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8') if isinstance(password_hash, bytes) else password_hash

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


# ------------------------------
# AthleteProfile
# ------------------------------
class AthleteProfile(db.Model, SerializerMixin):
    __tablename__ = "athlete_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)

    sport = db.Column(db.String)
    position = db.Column(db.String)
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    dob = db.Column(db.Date)
    injury_history = db.Column(db.Text)

    user = db.relationship('User', back_populates='athlete_profile')

    def __repr__(self):
        return f'<AthleteProfile user_id={self.user_id}>'


# ------------------------------
# Group & UserGroup
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

    def __repr__(self):
        return f'<Document id={self.id} title={self.title}>'


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
        viewonly=True
    )
    wellness_entry = db.relationship(
        "WellnessEntry",
        primaryjoin="and_(foreign(Comment.target_id)==WellnessEntry.id, Comment.target_type=='wellness_entry')",
        back_populates="comments",
        viewonly=True
    )

    def __repr__(self):
        return f'<Comment id={self.id} author={self.author_id} target={self.target_type}:{self.target_id}>'


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
