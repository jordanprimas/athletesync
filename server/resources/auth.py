

# ------------------------------
# Login  
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


# ------------------------------
# Authorize Session   
# ------------------------------
class AuthorizedSessionResource(Resource):
    def get(self):
        user_id = session.get('user_id')
        if not user_id:
            abort(401, "Unauthorized")

        user = User.query.get(user_id)
        if not user: 
            abort(401, "Unauthorized")

        return make_response(user.to_dict(), 200)

            

# ------------------------------
# Logout  
# ------------------------------
class LogoutResource(Resource):
    def delete(self):
        session.pop('user_id', None)
        return "", 204




# ------------------------------
# Sign-up   
# ------------------------------
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

