# ------------------------------
# USER  
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
            
