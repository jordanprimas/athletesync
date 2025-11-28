from flask import request, make_response, session, abort
from flask_restful import Resource

from ..models import GroupPost, db


# ------------------------------
# GROUP POST 
# ------------------------------
class GroupPostResource(Resource):
    def get(self):
        posts = GroupPost.query.all()
        if not posts:
            abort(404, "No posts were found.")
        
        return make_response([p.to_dict() for p in posts], 200)

    def post(self):
        data = request.get_json() or {}
        user_id = session.get("user_id")
        group_id = data.get("group_id")
        content = data.get("content")

        if not user_id:
            abort(401, "Unauthorized")
        if not group_id or not content:
            abort(400, "group_id and content are required.")

        new_post = GroupPost(
            group_id=group_id,
            author_id=user_id,
            content=content
        )

        db.session.add(new_post)
        db.session.commit()

        return make_response(new_post.to_dict(), 201)


# ------------------------------
# GROUP POST BY ID
# ------------------------------

class GroupPostByID(Resource):
    def get(self, id):
        post = GroupPost.query.get(id)
        if not post:
            abort(404, "Post not found.")
        return make_response(post.to_dict(), 200)

    def patch(self, id):
        post = GroupPost.query.get(id)
        if not post:
            abort(404, "Post not found.")

        user_id = session.get("user_id")
        if post.author_id != user_id:
            abort(403, "You can only edit your own post.")

        data = request.get_json() or {}
        if "content" in data:
            post.content = data["content"]

        db.session.commit()
        return make_response(post.to_dict(), 200)


    def delete(self, id):
        post = GroupPost.query.get(id)
        if not post:
            abort(404, "Post not found.")

        user_id = session.get("user_id")
        if post.author_id != user_id:
            abort(403, "You can only delete your own post.")

        db.session.delete(post)
        db.session.commit()

        return make_response({"message": "Post deleted", "id": id}, 200)

