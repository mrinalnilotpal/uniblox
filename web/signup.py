import json
import uuid
from .base_api import BaseAPI


class SignupAPI(BaseAPI):
    """API to handle user signup."""
    
    def __init__(self, signup_db):
        self.signup_db = signup_db

    def post(self):
        payload = self.get_payload()
        email = payload.get('email')

        with open(self.signup_db, 'r') as db_file:
            users = json.load(db_file)

        if any(user.get('email') == email for user in users):
            return {"message": "User already exists"}, 409

        new_user = {
            "_id": str(uuid.uuid4()),  
            **payload  
        }
        users.append(new_user)
        with open(self.signup_db, 'w') as db_file:
            json.dump(users, db_file, indent=4)

        return {"message": "User signed up successfully", "user": new_user["email"]}, 201

