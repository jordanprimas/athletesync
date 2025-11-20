from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
bcrypt = Bcrypt()


from .user import User
from .athlete_profile import AthleteProfile
from .group import Group
from .user_group import UserGroup
from .group_post import GroupPost
from .soap_note import SOAPNote
from .wellness_entry import WellnessEntry
from .document import Document
from .like import Like
from .comment import Comment
from .addendum import Addendum
