from flask import request, make_response, session, abort
from flask_restful import Resource

from ..models import AthleteProfile, User, db
from ..decorators.auth import require_role

# ------------------------------
# ATHLETE PROFILE 
# ------------------------------
class AthleteProfileResource(Resource):
    def get(self, id=None):
        user_id = session.get('user_id')
        if not user_id:
            abort(401, "Unauthorized")

        user = User.query.get(user_id)
        if not user:
            abort(401, "Unauthorized")

        if id is None:
            profile = AthleteProfile.query.filter_by(user_id=user_id).first()
            if not profile:
                abort(404, "Profile not found.")
            return make_response(profile.to_dict(), 200)

        if id != user.id and user.role != 'trainer':
            abort(403, "Forbidden: You can only view your own profile.")

        profile = AthleteProfile.query.filter_by(user_id=id).first()
        if not profile:
            abort(404, "Profile not found.")
        return make_response(profile.to_dict(), 200)

    @require_role('trainer')
    def post(self):
        data = request.get_json() or {}
        user_id = data.get('user_id')
        if not user_id:
            abort(400, "user_id is required.")
        if AthleteProfile.query.filter_by(user_id=user_id).first():
            abort(400, "Profile already exists.")

        profile = AthleteProfile(
            user_id=user_id,
            sport=data.get('sport'),
            position=data.get('position'),
            height=data.get('height'),
            weight=data.get('weight'),
            dob=data.get('dob'),
            injury_history=data.get('injury_history')
        )
        db.session.add(profile)
        db.session.commit()
        return make_response(profile.to_dict(), 201)

    @require_role('trainer')
    def patch(self, id):
        profile = AthleteProfile.query.get(id)
        if not profile:
            abort(404, "Profile not found.")

        data = request.get_json() or {}
        for attr in ['sport', 'position', 'height', 'weight', 'dob', 'injury_history']:
            if attr in data: 
                setattr(profile, attr, data[attr])

        db.session.commit()
        return make_response(profile.to_dict(), 200)