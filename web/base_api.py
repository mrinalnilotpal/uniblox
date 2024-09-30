
from flask import request, jsonify
from flask_restful import Resource
from functools import wraps

class BaseAPI(Resource):
    """Base class with shared functionality for all APIs."""
    
    def __init__(self, **kwargs):
        """Initialize the BaseAPI with any passed keyword arguments."""
        self.kwargs = kwargs

    def get_payload(self):
        """Get the payload from POST or GET requests."""
        if request.method == 'POST':
            return request.get_json(force=True)
        return request.args.to_dict()

    def response(self, message, status=200):
        """Standardized response method for returning JSON messages."""
        return jsonify({"message": message}), status


def admin_required(func):
    """Decorator to require admin access for specific API endpoints."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not request.headers.get('X-Admin-Token'):
            return {"error": "Admin access required"}, 403
        return func(*args, **kwargs)
    return wrapper

