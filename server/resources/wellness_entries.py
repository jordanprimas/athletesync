from flask import request, make_response, session, abort
from flask_restful import Resource

from ..models import WellnessEntry, User, Like, db
from ..decorators.auth import require_role
from datetime import datetime, timedelta

# ------------------------------
# WellnessEntry  
# ------------------------------
class WellnessEntryResource(Resource):
    @require_role("athlete")  # Only athletes can submit
    def post(self):
        data = request.get_json() or {}
        athlete_id = session.get("user_id")

        if not athlete_id:
            abort(401, "Unauthorized")

        entry = WellnessEntry(
            athlete_id=athlete_id,
            sleep_quality=data.get("sleep_quality"),
            mood=data.get("mood"),
            fatigue=data.get("fatigue"),
            soreness=data.get("soreness"),
            stress=data.get("stress"),
            pain=data.get("pain"),
            rehab_completed=data.get("rehab_completed", False),
            notes=data.get("notes")
        )

        db.session.add(entry)
        db.session.commit()

        return make_response(entry.to_dict(), 201)

class WellnessEntryById(Resource):
    @require_role("trainer")
    def get(self, id):
        entry = WellnessEntry.query.get(id)
        if not entry:
            abort(404, "Entry not found.")

        return make_response(entry.to_dict(), 200)

class WellnessEntryList(Resource):
    @require_role("trainer")
    def get(self):
        one_week_ago = datetime.utcnow() - timedelta(days=7)
        entries = WellnessEntry.query.filter(WellnessEntry.created_at >= one_week_ago).all()
        return make_response([e.to_dict() for e in entries], 200)
