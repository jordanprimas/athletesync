# decorators/auth.py
from functools import wraps
from flask import session, abort
from ..models import User  

def require_role(*roles):
    """
    Decorator to restrict access to users with specific roles.
    Usage:
        @require_role('trainer')
        def patch_soap_note(...):
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_id = session.get('user_id')
            if not user_id:
                abort(401, "Unauthorized: Please log in.")

            user = User.query.get(user_id)
            if not user:
                abort(401, "Unauthorized: User not found.")

            if user.role not in roles:
                abort(403, "Forbidden: You do not have permission to perform this action.")

            return func(*args, **kwargs)
        return wrapper
    return decorator
