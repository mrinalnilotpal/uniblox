import os
import json
import uuid
from .base_api import BaseAPI, admin_required

class AddProductAPI(BaseAPI):
    """API to add a new product (admin-only)."""

    def __init__(self, product_db):
        """
        Initialize the AddProductAPI with the path to the product database (JSON file).
        If the product database doesn't exist, create an empty JSON file.
        """
        self.product_db = product_db

        if not os.path.exists(self.product_db):
            with open(self.product_db, 'w') as db_file:
                json.dump([], db_file)

    @admin_required
    def post(self):
        """
        Handle POST request to add a new product.
        Only accessible by admins (protected by @admin_required decorator).
        """
        payload = self.get_payload()  
        company_name = payload.get('company', '').strip().lower()  
        product_name = payload.get('product', '').strip().lower()  

     
        with open(self.product_db, 'r') as db_file:
            products = json.load(db_file)

        
        if any(product['company'].strip().lower() == company_name and 
               product['product'].strip().lower() == product_name for product in products):
            return {"message": "Product already exists"}, 409 

 
        new_product = {
            "_id": str(uuid.uuid4()), 
            **payload  
        }
        products.append(new_product) 

        with open(self.product_db, 'w') as db_file:
            json.dump(products, db_file, indent=4)

  
        return {"message": "Product added successfully", "product": new_product}, 201 
