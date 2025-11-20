
# ------------------------------
# GROUP POST 
# ------------------------------
class GroupPostResource(Resource):
    def get(self):
        posts = [post.to_dict() for post in GroupPost.query.all()]

        if not posts:
            abort(404, "No posts were found!")
        
        response = make_response(
            posts, 
            200
        )

        return response

    def post(self):
        try:
            user_id = session['user_id']
            data = request.get_json()

            new_post = GroupPost(
                title = data.get('title'),
                content = data.get('content'),
                group_id=data.get("group_id"),
                user_id = user_id
            )

            db.session.add(new_post)
            db.session.commit()

            return make_response(new_post.to_dict(), 201)

        except ValueError as e:
            return {'error': str(e)}, 400




# ------------------------------
# GROUP POST BY ID
# ------------------------------

class GroupPostByID(Resource):
    def get(self, id):
        post = GroupPost.query.filter_by(id=id).first()
        if not post:
            abort(404, "The post you are looking for could not be found!")

        return make_response(post.to_dict(), 200)

    def patch(self, id):
        post = GroupPost.query.filter_by(id=id).first()
        if not post:
            abort(404, "Post not found.")

        user_id = session.get("user_id")
        if post.user_id != user_id:
            abort(403, "Not Allowed.")

        data = request.get_json()
        for attr, value in data.items():
            setattr(post, attr, value)

        db.session.commit()

        return make_response(post.to_dict(), 200)


    def delete(self, id):
        post = GroupPost.query.filter_by(id=id).first()
        if not post:
            abort(404, "The post you are trying to delete can't be found!")

        db.session.delete(post)
        db.session.commit()

        return make_response(
            {
                "delete_successful": True,
                "message": "Post deleted",
                "id": id
            },
            200
        )

