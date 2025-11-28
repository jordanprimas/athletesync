from flask import request, make_response, session, abort
from flask_restful import Resource

from ..models import Document, User, db
from ..decorators.auth import require_role

# ------------------------------
# Document
# ------------------------------
class DocumentResource(Resource):
    def get(self):
        user_id = session.get('user_id')
        if not user_id:
            abort(401, "Unathorized.")

        user = User.query.get(user_id)

        if user.role == 'trainer':
            docs = Document,query.all()
        else:
            docs = Document.query.filter_by(athlete_id=user_id).all()

        return make_response([doc.to_dict() for doc in docs], 200)

    @require_role("trainer")
    def post(self):
        data = request.get_json() or {}
        trainer_id = session.get('user_id')

        athlete_id = data.get("athlete_id")
        title = data.get("title")
        description = data.get("description")
        category = data.get("category")
        file_url = data.get("file_url")

        if not all ([athlete_id, title, file_url]):
            abort(400, "athlete_id, title, and file_url are required.")

        new_doc = Document(
            athlete_id=athlete_id,
            trainer_id=trainer_id,
            title=title,
            description=description,
            category=category,
            file_url=file_url
        )

        db.session.add(new_doc)
        db.session.commit()

        return make_response(new_doc.to_dict(), 201)


# ------------------------------
# Document By Id
# ------------------------------
class DocumentById(Resource):
    def get(self, id):
        user_id = session.get('user_id')
        if not user_id:
            abort(401, "Unauthorized.")

        user = User.query.get(user_id)
        doc = Document.query.get(id)
        if not doc:
            abort(404, "Document not found.")

        if user.role == 'trainer' or doc.athlete_id == user_id:
            return make_response(doc.to_dict(), 200)
        else:
            abort(403, "Forbidden: You cannot access this document.")