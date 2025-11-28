import os
import secrets
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
SESSION_DIR = os.path.join(BASE_DIR, "flask_session")


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY") or secrets.token_hex(24)

    SESSION_TYPE = "filesystem"
    SESSION_FILE_DIR = SESSION_DIR
    SESSION_PERMANENT = True

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(INSTANCE_DIR, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    

    
