# resources/like.py

from flask import request, make_response, session, abort
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from ..models import db, Like, GroupPost, WellnessEntry


TARGET_MODELS = {
    "post": GroupPost,
    "wellness_entry": WellnessEntry,
}

# Allowed like types
LIKE_TYPES = {"like", "verify"}


class LikeResource(Resource):
    def get(self):
        likes = Like.query.all()
        if not likes:
            abort(404, "No likes found.")
        return make_response([l.to_dict() for l in likes], 200)

    def post(self):
        user_id = session.get("user_id")
        if not user_id:
            abort(401, "Unauthorized. Please log in.")

        data = request.get_json() or {}
        target_type = data.get("target_type")
        target_id = data.get("target_id")
        like_type = data.get("like_type", "like")

        if not target_type or not target_id:
            abort(400, "target_type and target_id are required.")
        if target_type not in TARGET_MODELS:
            abort(400, f"Invalid target_type: {target_type}")
        if like_type not in LIKE_TYPES:
            abort(400, f"Invalid like_type: {like_type}")

        
        Model = TARGET_MODELS[target_type]
        if not Model.query.get(target_id):
            abort(404, f"{target_type} not found.")

       
        existing_like = Like.query.filter_by(
            user_id=user_id, target_type=target_type, target_id=target_id
        ).first()
        if existing_like:
            abort(400, "You already liked this.")

        new_like = Like(
            user_id=user_id,
            target_type=target_type,
            target_id=target_id,
            like_type=like_type,
        )

        db.session.add(new_like)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(400, "You already liked this.")

        return make_response(new_like.to_dict(), 201)


class LikeByID(Resource):
    def delete(self, id):
        user_id = session.get("user_id")
        if not user_id:
            abort(401, "Unauthorized.")

        like = Like.query.get(id)
        if not like:
            abort(404, "Like not found.")
        if like.user_id != user_id:
            abort(403, "You cannot delete another user's like.")

        db.session.delete(like)
        db.session.commit()

        return make_response({
            "delete_successful": True,
            "message": "Like deleted",
            "id": id
        }, 200)
