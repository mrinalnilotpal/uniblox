
import os
import json
from .base_api import BaseAPI

class AddToCartAPI(BaseAPI):
    """API to add items to cart."""

    def __init__(self, signup_db):
        self.signup_db = signup_db

        if not os.path.exists(self.signup_db):
            with open(self.signup_db, 'w') as db_file:
                json.dump([], db_file)  

    def post(self):
        payload = self.get_payload()
        client_id = payload.get('client_id')
        product_id = payload.get('product_id')

        with open(self.signup_db, 'r') as db_file:
            users = json.load(db_file)

        user = next((user for user in users if user.get('_id') == client_id), None)

        if user is None:
            return {"message": "User not found"}, 404  

  
        if 'cart' not in user:
            user['cart'] = []  

      
        if product_id not in user['cart']:
            user['cart'].append(product_id)

            with open(self.signup_db, 'w') as db_file:
                json.dump(users, db_file, indent=4)

            return {"message": "Product added to cart"}, 200  # OK
        else:
            return {"message": "Product already in cart"}, 409  # Conflict

        
