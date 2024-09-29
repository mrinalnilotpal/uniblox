import os
import json
import uuid
from .base_api import BaseAPI

class CheckoutAPI(BaseAPI):
    def __init__(self, nth_order, product_db, signup_db, orders_db):
        self.nth_order = nth_order
        self.product_db = product_db
        self.signup_db = signup_db
        self.orders_db = orders_db

    def _get_user(self, client_id):
        """Fetch the user by client_id."""
        with open(self.signup_db, 'r') as signup_file:
            users = json.load(signup_file)
        user = next((u for u in users if u["_id"] == client_id), None)
        return user, users

    def _calculate_total_amount(self, cart):
        """Calculate the total amount based on items in the cart."""
        with open(self.product_db, 'r') as product_file:
            products = json.load(product_file)
        return sum(prod["price"] for prod in products if prod["_id"] in cart)

    def _process_discount(self, user, total_amount, order_count, coupon_req):
        """Apply discount logic based on the order count."""
        current_block_start = (order_count // self.nth_order) * self.nth_order
        current_block_end = current_block_start + self.nth_order - 1

        print(current_block_start,order_count,current_block_end)
        if current_block_start <= order_count and order_count <= current_block_end:
            if coupon_req and user.get('stored_discount') is not None:
                discount = total_amount * 0.10
                total_amount -= discount
                user['stored_discount'] = None  # Mark discount as used
                return discount
        
        if order_count == current_block_start:
            #if not user.get('stored_discount'):
                user['stored_discount'] = f"DISCOUNT_10_{order_count}"


    def _create_order(self, client_id, cart, total_amount, discount, stored_discount):
        """Create a new order object."""
        order_id = str(uuid.uuid4())
        return {
            "order_id": order_id,
            "user_id": client_id,
            "items_purchased": len(cart),
            "items": cart,
            "total_purchase_amount": total_amount,
            "discount_codes": [stored_discount] if discount else [],
            "total_discount_amount": discount
        }

    def _save_order(self, new_order):
        """Save the new order to the orders database."""
        with open(self.orders_db, 'r+') as orders_file:
            orders = json.load(orders_file)
            orders.append(new_order)
            orders_file.seek(0)
            json.dump(orders, orders_file, indent=4)

    def _update_user(self, user, users, order_id):
        """Update the user data after checkout."""
        user['order_ids'] = user.get('order_ids', []) + [order_id]
        user['cart'] = []

        # Update the users list and write back to the file
        with open(self.signup_db, 'w') as signup_file:
            json.dump(users, signup_file, indent=4)

    def post(self):
        """Handle the checkout process."""
        payload = self.get_payload()
        client_id = payload.get('client_id')
        coupon_req = payload.get('coupon_req')

        # Validate client_id
        if not client_id:
            return {"message": "client_id is required"}, 400

        user, users = self._get_user(client_id)
       
        if not user:
            return {"message": "User not found"}, 404

        cart = user.get('cart', [])
      
        if not cart:
            return {"message": "Cart is empty"}, 400

        total_amount = self._calculate_total_amount(cart)

        order_count = len(user.get('order_ids', [])) + 1
        print(order_count)
        discount = 0
        if order_count >= self.nth_order:
            discount = self._process_discount(user, total_amount, order_count, coupon_req)
            st_discount = user['stored_discount']
            print(st_discount)
        
        new_order = self._create_order(client_id, cart, total_amount, discount, st_discount)

        self._save_order(new_order)
        self._update_user(user, users, new_order['order_id'])

        return {"message": "Checkout successful", "order": new_order}, 201
