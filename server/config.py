from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_session import Session
import secrets
import os
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv


# Instantiate Flask app object, set attributes
app = Flask(__name__)


#Generate and set secret key
app.secret_key = secrets.token_hex(24)

bcrypt = Bcrypt(app)

# Define metadata, instantiate db
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)

# Configure a database connection to the local file app.db 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
# Disable modification tracking to use less memory 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Ensure each key/value json pair is displayed on a separate line 
app.json.compact = False

# Create a Migrate object to manage schema modifications 
migrate = Migrate(app, db)
# Initialize the Flask application to use the database 
db.init_app(app)




app.config['SESSION_TYPE'] = 'filesystem'
app.config['SERVER_NAME'] = 'localhost:5555'

app.config['SESSION_PERMANENT'] = True
app.json.compact = False

Session(app)



# Instantiate REST API
api = Api(app)

# Instantiate CORS
CORS(app)

# Configure oauth
oauth = OAuth(app)

load_dotenv()
google = oauth.register(
    name='google',
    client_id= os.getenv('CLIENT_ID'),
    client_secret= os.getenv('CLIENT_SECRET'),
    access_token_url='https://oauth2.googleapis.com/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'email profile'},
    # scope - what google will return to us this information in the user_info variable in app.py route
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration'
)


