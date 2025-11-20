#!/usr/bin/env python3

from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_session import Session

# Local imports
from config import Config
from models import db  
from resources import *

# ------------------------------
# Initialize Flask app
# ------------------------------
app = Flask(__name__)
app.config.from_object(Config)

# ------------------------------
# Initialize extensions
# ------------------------------
db.init_app(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
Session(app)
CORS(app)
api = Api(app)

# ------------------------------
# Database setup
# ------------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SERVER_NAME'] = 'localhost:5555'
db = SQLAlchemy(app)
migrate = Migrate(app, db)




# ------------------------------
# Register API resources
# ------------------------------
api.add_resource(LoginResource, '/api/login')
api.add_resource(SignupResource, '/api/signup')
api.add_resource(AuthorizedSessionResource, '/api/authorized')
api.add_resource(LogoutResource, '/api/logout')

api.add_resource(UserResource, '/api/users')

api.add_resource(AthleteProfileResource, '/api/athlete_profiles')

api.add_resource(GroupResource, '/api/groups')
api.add_resource(GroupByID, '/api/groups/<int:id>')
api.add_resource(UserGroupResource, '/api/user_groups')
api.add_resource(UserGroupById, '/api/user_groups/<int:id>')

api.add_resource(SOAPNoteResource, '/api/soap_notes')
api.add_resource(SOAPNoteById, '/api/soap_notes/<int:id>')

api.add_resource(WellnessEntryResource, '/api/wellness_entries')
api.add_resource(WellnessEntryById, '/api/wellness_entries/<int:id>')

api.add_resource(DocumentResource, '/api/documents')
api.add_resource(DocumentById, '/api/documents/<int:id>')

api.add_resource(LikeResource, '/api/likes')
api.add_resource(LikeByID, '/api/likes/<int:id>')

api.add_resource(CommentResource, '/api/comments')
api.add_resource(CommentById, '/api/comments/<int:id>')

api.add_resource(AddendumResource, '/api/addendums')
api.add_resource(AddendumById, '/api/addendums/<int:id>')

# ------------------------------
# Run app
# ------------------------------
if __name__ == '__main__':
    app.run(port=5555, debug=True)


















# @app.route('/google')
# def google_login():
#     google = oauth.create_client('google')
#     state = secrets.token_urlsafe(16)
    
#     session['oauth_state'] = state
    
#     redirect_uri = url_for('google_auth', _external=True)
#     return google.authorize_redirect(redirect_uri, state=state)


# @app.route('/google/auth')
# def google_auth():
#     state = request.args.get('state')
#     print("Google auth state:", state)
#     google = oauth.create_client('google') #
#     print("google", google)
#     token = google.authorize_access_token()
#     print("token", token)
#     resp = google.get('userinfo')
#     user_info = resp.json()
    
#     try:
        
#         existing_user = User.query.filter_by(email=user_info['email']).first()

#         if existing_user:
#             session['user_id'] = existing_user.id
#             return redirect('http://localhost:3000') 
#         else:
#             new_user = User(
#                 username=user_info['email'],
#                 email=user_info['email'],
#             )
#             db.session.add(new_user)
#             db.session.commit()
#             session['user_id'] = new_user.id
#             return redirect('http://localhost:3000') 
#     except Exception as e:
#         print("Exception during Google OAuth:", e)
#         abort(401, "Unauthorized")







