from flask import request, make_response, session, abort
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from ..models import User, Group, UserGroup, db


# ------------------------------
# GROUP 
# ------------------------------

class GroupResource(Resource): 
    def get(self):
        groups = Group.query.all()
        if not groups:
            abort(404, "No groups were found.")
        
        return make_response([g.to_dict() for g in groups], 200)

        
    def post(self):
        data = request.get_json() or {}
        name = data.get("name")
        description = data.get("description")
        cover_image = data.get("cover_image")

        if "name" in data and not data["name"]:
            abort(400, "Group name is required.")
            

        try:
            new_group = Group(
                name=name,
                description=description,
                cover_image=cover_image
            )

            db.session.add(new_group)
            db.session.commit()

            return make_response(new_group.to_dict(), 201)

        except IntegrityError:
            db.session.rollback()
            abort(400, "A group with that name already exists")
        except ValueError as e:
            db.session.rollback()
            abort(400, str(e))

 


# ------------------------------
# GROUP BY ID
# ------------------------------

class GroupByID(Resource):
    def get(self, id):
        group = Group.query.filter_by(id=id).first()
        if not group:
            abort(404, "Group not found.")
        
        return make_response(group.to_dict(), 200)
        

    def patch(self, id):
        group = Group.query.filter_by(id=id).first()
        if not group:
            abort(404, "Group not found.") 

        data = request.get_json() or {}

        for attr in ["name", "description", "cover_image"]:
            if attr in data:
                setattr(group, attr, data[attr])

        try:
            db.session.commit()
            return make_response(group.to_dict(), 200)
        except IntegrityError:
            db.session.rollback()
            abort(400, "A group with that name already exists.")
        except ValueError as e:
            db.session.rollback()
            abort(400, str(e))


    def delete(self, id):
        group = Group.query.filter_by(id=id).first()
        if not group:
            abort(404, "Group not found.") 

        db.session.delete(group)
        db.session.commit()

        return "", 204



# ------------------------------
# USER-GROUP ASSOCIATION
# ------------------------------

class UserGroupResource(Resource):
    def get(self):
        user_groups = UserGroup.query.all()
        if not user_groups:
            abort(404, "No user-group relationships found.")
        
        return make_response([ug.to_dict() for ug in user_groups], 200)

    def post(self):
        data = request.get_json() or {}
        user_id = session.get('user_id')
        group_id = data.get('group_id')

        if not user_id:
            abort(401, "Unauthorized. Please log in.")
        if not group_id:
            abort(400, "group_id is required.")

        group = Group.query.get(group_id)
        if not group:
            abort(404, "Group not found")

        # Check for existing group membership  
        existing = UserGroup.query.filter_by(user_id=user_id, group_id=group_id).first()
        if existing:
            abort(400, "User is already in this group.")
           
        new_user_group = UserGroup(user_id=user_id, group_id=group_id)
                
        db.session.add(new_user_group)
        db.session.commit()

        return make_response(new_user_group.to_dict(), 201)




# ------------------------------
# USER-GROUP BY ID 
# ------------------------------

class UserGroupById(Resource):
    def delete(self, id):
        user_group = UserGroup.query.filter_by(id=id).first()

        if not user_group:
            abort(404, "User-group relationship not found.")
        
        db.session.delete(user_group)
        db.session.commit()

        return {
            "message": "User removed from group",
            "id": id
        }, 200
       

