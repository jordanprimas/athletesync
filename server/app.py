#!/usr/bin/env python3
import os
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_migrate import Migrate
from flask_session import Session

from .config import Config
from .models import db, bcrypt
from .resources import *

def create_app():
    instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "instance")
    os.makedirs(instance_path, exist_ok=True)

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    Migrate(app, db)
    Session(app)
    CORS(app)
    api = Api(app)

    # Register resources
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

    return app

app = create_app()

if __name__ == '__main__':
    app.run(port=5555, debug=True)
