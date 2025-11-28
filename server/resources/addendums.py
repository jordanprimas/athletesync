from flask import request, make_response, session, abort
from flask_restful import Resource

from ..models import Addendum, User, db
from ..decorators.auth import require_role

# ------------------------------
# Addendum
# ------------------------------
class AddendumResource(Resource):
    def get(self):
        user_role = session.get("role")
        user_id = session.get("user_id")

        if not user_role == "trainer":
            addendums = Addendum.query.all()
        return make_response([a.to_dict() for a in addendums], 200)

    @require_role("trainer")
    def post(self):
        data = request.get_json() or {}
        author_id = session.get("user_id")

        target_type = data.get("target_type")
        target_id = data.get("target_id")
        content = data.get("content")
        annotation_type = data.get("annotation_type", "revision")

        if not target_type or not target_id or not content:
            abort(400, "target_type, target_id, and content are required.")

        valid_types = ["wellness_entry", "soap_note", "document"]
        if target_type not in valid_types:
            abort(400, f"Invalid target_type: {target_type}")

        addendum = Addendum(
            author_id=author_id,
            target_type=target_type,
            target_id=target_id,
            content=content,
            annotation_type=annotation_type
        )

        db.session.add(addendum)
        db.session.commit()

        return make_response(addendum.to_dict(), 201)


# ------------------------------
# Addeundum By ID 
# ------------------------------
class AddendumById(Resource):
    def get(self, id):
        addendum = Addendum.query.get(id)
        if not addendum:
            abort(404, "Addendum not found.")

        user_role = session.get("role")

        if not user_id:
            abort(401, "Unauthorized")
            
        return make_response(addendum.to_dict(), 200)