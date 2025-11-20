# ------------------------------
# LIKE 
# ------------------------------

class LikeResource(Resource):
    def get(self):
        likes = Like.query.all()
        if not likes: 
            abort(404, "No likes found.")
            
        return make_response([l.to_dict() for l in likes], 200)
    
    def post(self):
        data = request.get_json() or {}

        user_id = session.get('user_id')
        if not user_id:
            abort(401, "Unauthorized. Please log in.")

        target_type = data.get("target_type")
        target_id = data.get("target_id")

        if not target_type:
            abort(400, "target_type is required.")
        if not target_id:
            abort(400, "target_id is required.")

        if target_type not in ("post", "wellness_entry"):
            abort(400, "Invalid target_type.")

        existing_like = Like.query.filter_by(user_id=user_id, target_type=target_type, target_id=target_id).first()
        
        if existing_like:
            abort(400, "You already liked this.")
   
        new_like = Like(
            user_id=user_id, 
            target_type=target_type,
            target_id=target_id,
            like_type=data.get("like_type", "like")
        )

        db.session.add(new_like)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(400, "You already liked this.")
        
        return make_response(new_like.to_dict(), 201)




# ------------------------------
# LIKE BY ID 
# ------------------------------

class LikeByID(Resource):
    def delete(self, id):
        user_id = session.get("user_id")
        if not user_id:
            abort(401, "Unauthorized.")

        like = Like.query.filter_by(id=id).first()
        if not like:
            abort(404, "Like not found.")

        if like.user_id != user_id:
            abort(403, "You cannot delete another user's like.")

        db.session.delete(like)
        db.session.commit()

        response_body = {
            "delete_successful": True,
            "message": "Like deleted",
            "id": id
        }
        
        return {
            "message": "Like deleted.",
            "id": id
        }, 200



