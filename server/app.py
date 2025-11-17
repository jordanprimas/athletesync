#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, make_response, session, abort, url_for, redirect
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

# Local imports
from config import app, api, db, oauth, secrets, google
from models import User, AthleteProfile, Group, UserGroup, SOAPNote, WellnessEntry, Document, GroupPost, Comment, Like, Addendum



# @app.route('/google')
# def google_login():
#     google = oauth.create_client('google')
#     state = secrets.token_urlsafe(16)
    
#     session['oauth_state'] = state
    
#     redirect_uri = url_for('google_auth', _external=True)
#     return google.authorize_redirect(redirect_uri, state=state)


# @app.route('/google/auth')
# def google_auth():
#     state = request.args.get('state')
#     print("Google auth state:", state)
#     google = oauth.create_client('google') #
#     print("google", google)
#     token = google.authorize_access_token()
#     print("token", token)
#     resp = google.get('userinfo')
#     user_info = resp.json()
    
#     try:
        
#         existing_user = User.query.filter_by(email=user_info['email']).first()

#         if existing_user:
#             session['user_id'] = existing_user.id
#             return redirect('http://localhost:3000') 
#         else:
#             new_user = User(
#                 username=user_info['email'],
#                 email=user_info['email'],
#             )
#             db.session.add(new_user)
#             db.session.commit()
#             session['user_id'] = new_user.id
#             return redirect('http://localhost:3000') 
#     except Exception as e:
#         print("Exception during Google OAuth:", e)
#         abort(401, "Unauthorized")



# ------------------------------
# Authorization 
# ------------------------------
class LoginResource(Resource):
    def post(self):
        data = request.get_json() or {}
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            abort(400, "Username and password are required.")
        
        user = User.query.filter_by(username=username).first()

        if not user or not user.authenticate(password):
            abort(401, "Incorrect username or password.")

        session['user_id'] = user.id
        return make_response(user.to_dict(), 200)

api.add_resource(LoginResource, '/api/login')


class AuthorizedSessionResource(Resource):
    def get(self):
        user_id = session.get('user_id')
        if not user_id:
            abort(401, "Unauthorized")

        user = User.query.get(user_id)
        if not user: 
            abort(401, "Unauthorized")

        return make_response(user.to_dict(), 200)

api.add_resource(AuthorizedSessionResource, '/api/authorized')
            

class LogoutResource(Resource):
    def delete(self):
        session.pop('user_id', None)
        return {"message": "Logged out"}, 204

api.add_resource(LogoutResource, '/api/logout')

class SignupResource(Resource):
    def post(self):
        data = request.get_json()
        
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'athlete')

        if not all([username, email, password]):
            abort(400, "Username, email, and password are required.")
        
        try:
            new_user = User(
                username=username,
                email=email,
                role=role,
            )
            new_user.password_hash = password

            db.session.add(new_user)
            db.session.commit()

            session['user_id'] = new_user.id

            return make_response(new_user.to_dict(), 201)

        except IntegrityError:
            db.session.rollback()
            abort(400, "Username or email already exists.")
        except ValueError as e:
            db.session.rollback()
            abort(400, str(e))

api.add_resource(SignupResource, '/api/signup')


# ------------------------------
# USER Resource 
# ------------------------------
class UserResource(Resource):
    def get(self):
        users = [user.to_dict() for user in User.query.all()]
        if not users:
            abort(404, "No users were found.")
        return make_response(users, 200)


    def post(self):
        data = request.get_json() or {}
        
        username=data.get('username')
        email=data.get('email')
        password=data.get('password')
        role = data.get('role', 'athlete')
        photo_url=data.get('photo_url') or None 

        if not all([username, email, password]):
            abort(400, "Username, email, and password are required.")
        
        try:
            new_user = User(
                username=username,
                email=email,
                role=role,
                photo_url=photo_url,
            )
            new_user.password_hash = password 
            
            db.session.add(new_user)
            db.session.commit()

            session['user_id'] = new_user.id
            return make_response(new_user.to_dict(), 201)

        except IntegrityError:
            db.session.rollback()
            abort(400, "Username or email already exists.")
        except ValueError as e:
            db.session.rollback()
            abort(400, str(e))
            
api.add_resource(UserResource, '/api/users')

# ------------------------------
# GROUP-POST Resource
# ------------------------------
class AllGroupPostResource(Resource):
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

api.add_resource(AllGroupPost, "/api/group_posts")

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

api.add_resource(GroupPostByID, '/api/group_posts/<int:id>')


# ------------------------------
# GROUP Resource
# ------------------------------
class AllGroupResource(Resource): 
    def get(self):
        groups = [group.to_dict() for group in Group.query.all()]
        if not groups:
            abort(404, "No groups were found!")

        response = make_response(
            groups,
            200
        )

        return response
    
    def post(self):
        try:
            data = request.get_json()

            new_group = Group(
                name=data.get("name"),
            )


            db.session.add(new_group)
            db.session.commit()

            new_group_dict = new_group.to_dict()

            response = make_response(
                new_group_dict,
                201
            )
            return response
        except ValueError as e:
            return {'error': str(e)}, 400

api.add_resource(AllGroupResource, "/api/groups")  

class GroupByID(Resource):
    def get(self, id):
        group = Group.query.filter_by(id=id).first().to_dict()
        if not group:
            abort(404, "The group you are looking for could not be found!")
        
        response = make_response(
            group,
            200
        )
        return response
        

    def patch(self, id):
        group = Group.query.filter_by(id=id).first()
        if not group:
            abort(404, "The group you are trying to update could not be found!") 
        data = request.get_json()
        for attr in ["name", "description", "cover_image"]:
            if attr in data:
                setattr(group, attr, data[attr])
        db.session.add(group)
        db.session.commit()

        response_dict = group.to_dict()
        response = make_response(
            group,
            200
        )
        return response
    
    def delete(self, id):
        group = Group.query.filter_by(id=id).first()
        if not group:
            abort(404, "The group you are trying to delete could not be found!") 

        db.session.delete(group)
        db.session.commit()
        return {}, 204

api.add_resource(GroupByID, "/api/groups/<int:id>")



# ------------------------------
# USERGROUP Association Resource
# ------------------------------
class UserGroupResource(Resource):
    def get(self):
        user_groups = [user_group.to_dict() for user_group in UserGroup.query.all()]

        if not user_groups:
            abort(404, "No user groups were found!")
        
        response = make_response(
            user_groups, 
            200
        )

        return response

    def post(self):
        data = request.get_json()
        user_id = session['user_id']
        group_id = data.get('group_id')

        existing_user_group = UserGroup.query.filter_by(user_id=user_id, group_id=group_id).first()

        if existing_user_group:
            response_body = {
                "error": "User already in this group"
            }
            response = make_response(
                response_body,
                400
            )
            return response

        else:
            try:
                new_user_group = UserGroup(
                    user_id=user_id,
                    group_id=group_id
                )

                db.session.add(new_user_group)
                db.session.commit()

                return make_response(new_user_group.to_dict(), 201)

            except ValueError as e:
                return {'error': str(e)}, 400

api.add_resource(UserGroupResource, "/api/user_groups")

class UserGroupById(Resource):
    def delete(self, id):
        user_group = UserGroup.query.filter_by(id=id).first()

        if not user_group:
            abort(404, "The user group you are trying to delete can't be found")
        
        db.session.delete(user_group)
        db.session.commit()

        response_body = {
            "delete_successful": True,
            "message": "Post deleted",
            "id": id
        }
        response = make_response(
            response_body,
            200
        )
        return response

api.add_resource(UserGroupById, "/api/user_groups/<int:id>")

# ------------------------------
# LIKE Resource
# ------------------------------
class LikeResource(Resource):
    def get(self):
        likes = [like.to_dict() for like in Like.query.all()]
        if not likes: 
            abort(404, "No likes were found")
            
        response = make_response(
                likes, 
                200
            )
        return response
    
    def post(self):
        data = request.get_json()
        user_id = data.get('user_id')
        post_id = data.get('post_id')

        existing_like = Like.query.filter_by(user_id=user_id, post_id=post_id).first()
        if existing_like:
            response_body = {
                "error":"User already liked this post",
            }
            response = make_response(
                response_body,
                400
            )
            return response 

        new_like = Like(
            user_id=user_id, 
            post_id=post_id 
        )

        db.session.add(new_like)
        db.session.commit()

        new_like_dict = new_like.to_dict()

        response = make_response(
            new_like_dict,
            200
        )

        return response
api.add_resource(LikeResource, "/api/likes")

class LikeByID(Resource):
    def delete(self, id):
        like = Like.query.filter_by(id=id).first()
        if not like:
            abort(404, "The like you are trying to delete can't be found!")

        db.session.delete(like)
        db.session.commit()

        response_body = {
            "delete_successful": True,
            "message": "Like deleted",
            "id": id
        }
        response = make_response(
            response_body,
            200
        )
        return response

api.add_resource(LikeByID, '/api/likes/<int:id>')







# app.run() method to run development server treating application as a script 
if __name__ == '__main__':
    app.run(port=5555, debug=True)
