import json
from .base_api import BaseAPI
from flask import request


class LoginAPI(BaseAPI):
    """API to handle user login."""

    def __init__(self, signup_db):
        self.signup_db = signup_db

    def post(self):
        payload = self.get_payload()
        email = payload.get('email')
        password = payload.get('password')

        with open(self.signup_db, 'r') as db_file:
            users = json.load(db_file)

        user = next((user for user in users if user.get('email') == email), None)

        if user is None:
            return {"message": "User doesn't exist"}, 404  

        if user.get('password') != password:
            return {"message": "Incorrect password"}, 401

        return {"message": "Login successful"}, 200
