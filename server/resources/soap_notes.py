from flask import request, make_response, session, abort
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from ..models import User, SOAPNote, db
from ..decorators.auth import require_role

# ------------------------------
# SOAPNote 
# ------------------------------
class SOAPNoteResource(Resource):
    def get(self, athlete_id=None):
        user_id = session.get('user_id')
        if not user_id:
            abort(401, "Unauthorized")

        user = User.query.get('user_id')

        if user.role == 'athlete':
            notes = SOAPNote.query.filter_by(athlete_id=user_id).all()
        else:
            if athlete_id:
                notes = SOAPNote.query.filter_by(athlete_id=athlete_id).all()
            else:
                notes = SOAPNote.query.all()

        return make_response([note.to_dict() for note in notes], 200)


        @require_role('trainer')
        def post(self):
            data = request.get_json() or {}
            user_id = session.get('user_id')

            athlete_id = data.get('athlete_id')
            if not athlete_id:
                abort(400, "athlete_id is required")

            new_note = SOAPNote(
                athlete_id=athlete_id,
                trainer_id=user_id,
                subjective=data.get('subjective'),
                objective=data.get('objective'),
                assessment=data.get('assessment'),
                plan=data.get('plan'),
                injury_location=data.get('injury_location'),
                injury_type=data.get('injury_type')
            )

            try: 
                db.session.add(new_note)
                db.session.commit()
                return make_response(new_note.to_dict(), 201)
            except IntegrityError:
                db.session.rollback()
                abort(400, str(e))

# ------------------------------
# SOAPNote By ID  
# ------------------------------
class SOAPNoteById(Resource):
    def get(self, id):
        user_id = session.get('user_id')
        if not user_id:
            abort(401, "Unauthorized.")

        note = SOAPNOTE.query.get(id)
        if not note:
            abort(404, "SOAPNote not found.")

        user = User.query.get(user_id)

        if user.role == 'athlete' and note.athlete_id != user_id:
            abort(403, "Not allowed.")

        return make_response(note.to_dict(), 200)

    @require_role('trainer')
    def patch(self, id):
        note = SOAPNote.query.get(id)
        if not note:
            abort(404, "SOAPNote not found.")

        data = request.get_json() or {}
        for attr in ['subjective', 'objective', 'assessment', 'plan', 'injury_location', 'injury_type']:
            if attr in data:
                setattr(note, attr, data[attr])

        try:
            db.session.commit()
            return make_response(note.to_dict(), 200)
        except ValueError as e:
            db.session.rollback()
            abort(400, str(e))

    @require_role('trainer')
    def delete(self, id):
        note = SOAPNote.query.get(id)
        if not note:
            abort(404, "SOAPNote not found.")

        db.session.delete(note)
        db.session.commit()
        return {"message": "SOAPNote deleted."}, 204
