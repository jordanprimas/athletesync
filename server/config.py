import os
import secrets
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Secret key for sessions
    SECRET_KEY = os.getenv("SECRET_KEY") or secrets.token_hex(24)

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI") or "sqlite:///app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session configuration
    SESSION_TYPE = "filesystem"
    SESSION_PERMANENT = True






