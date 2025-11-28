from flask import request, make_response, session, abort
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from ..models import Comment, GroupPost, WellnessEntry, SOAPNote, User, db

# ------------------------------
# Comment
# ------------------------------
class CommentResource(Resource):
    def get(self):
        comments = Comment.query.all()
        if not comments:
            abort(404, "No comments found.")
        return make_response([c.to_dict() for c in comments], 200)

    def post(self):
        data = request.get_json() or {}
        user_id = session.get('user_id')
        if not user_id:
            abort(401, "Unauthorized. Please log in.")

        target_type = data.get('target_type')
        target_id = data.get('target_id')
        message = data.get('message')

        if not all([target_type, target_id, message]):
            abort(400, "target_type, target_id, and message are required.")

        user = User.query.get(user_id)
        if not user:
            abort(401, "Unauthorized. User not found.")

        if target_type in ['wellness_entry', 'soap_note'] and user.role != 'trainer':
            abort(403, "Unauthorized to comment on this type of entry.")
        
        if target_type == 'post':
            if not GroupPost.query.get(target_id):
                abort(404, "Post not found.")
        elif target_type == 'wellness_entry':
            if not WellnessEntry.query.get(target_id):
                abort(404, "Wellness entry not found.")
        elif target_type == 'soap_note':
            if not SOAPNote.query.get(target_id):
                abort(404, "SOAP note not found.")
        else:
            abort(400, "Invalid target_type.")

        try:
            new_comment = Comment(
                author_id=user_id,
                target_type=target_type,
                target_id=target_id,
                message=message
            )
            db.session.add(new_comment)
            db.session.commit()
            return make_response(new_comment.to_dict(), 201)
        except IntegrityError as e:
            db.session.rollback()
            abort(400, f"Error creating comment: {str(e)}")


# ------------------------------
# Comment By Id
# ------------------------------
class CommentById(Resource):
    def patch(self, id):
        comment = Comment.query.get(id)
        if not comment:
            abort(404, "Comment not found.")

        user_id = session.get('user-id')
        if not user_id:
            abort(401, "Unauthorized. Please log in.")

        if comment.target_type == 'post':
            if comment.author_id != user_id:
                abort(403, "You can only edit your own post comments.")
        else:
            user = User.query.get(user_id)
            if user.role != 'trainer':
                abort(403, "Unauthorized to edit this comment.")
        
        data = request.get_json() or {}
        if 'message' in data:
            comment.message = data['message']

        db.session.commit()
        return make_response(comment.to_dict(), 200)


    def delete(self, id):
        comment = Comment.query.get(id)
        if not comment:
            abort(404, "Comment not found.")

        user_id = session.get(user_id)
        if not user_id:
            abort(401, "Unauthorized. Please log in.")
        
        if comment.target_type == 'post':
            if comment.author_id != user_id:
                abort(403, "You can only delete your own post comments.")
        else:
            user = User.query.get(user_id)
            if user.role != 'trainer':
                abort(403, "Only trainers can delete this comment.")

        db.session.delete(comment)
        db.session.commit()
        return {"message": "Comment deleted", "id": id}, 200

