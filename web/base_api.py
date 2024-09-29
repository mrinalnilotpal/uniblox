
from flask import request, jsonify
from flask_restful import Resource
from functools import wraps

class BaseAPI(Resource):
    """Base class with shared functionality for all APIs."""
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def get_payload(self):
        """Get the payload from POST or GET requests."""
        if request.method == 'POST':
            return request.get_json(force=True)
        return request.args.to_dict()

    def response(self, message, status=200):
        """Standardized response method."""
        return jsonify({"message": message}), status


# Decorator to require admin privileges
def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not request.headers.get('X-Admin-Token'):
            return {"error": "Admin access required"}, 403
        return func(*args, **kwargs)
    return wrapper
