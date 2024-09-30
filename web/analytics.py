import os
import json
import pandas as pd
from .base_api import BaseAPI

class GenerateAnalysisAPI(BaseAPI):
    def __init__(self, product_db, signup_db, orders_db):
        """Initialize the GenerateAnalysisAPI with product, signup, and orders databases."""
        self.product_db = product_db
        self.signup_db = signup_db
        self.orders_db = orders_db

    def get(self):
        """Handle GET request to generate analysis based on signup and order data."""
        with open(self.signup_db, 'r') as f:
            signup_data = json.load(f)
        with open(self.orders_db, 'r') as f:
            orders_data = json.load(f)
        with open(self.product_db, 'r') as f:
            product_data = json.load(f)

        df_signup = pd.DataFrame(signup_data)
        df_orders = pd.DataFrame(orders_data)

        df_orders['discount_codes'] = df_orders['discount_codes'].apply(lambda x: [] if x is None else x)
        df_orders['total_discount_amount'] = df_orders['total_discount_amount'].fillna(0)

        user_summary = df_orders.groupby('user_id').agg(
            total_items_purchased=('items_purchased', 'sum'),
            total_purchase_amount=('total_purchase_amount', 'sum'),

            discount_codes=('discount_codes', lambda x: [code for sublist in x for code in sublist if code]),
            total_discount_amount=('total_discount_amount', 'sum')
        ).reset_index()

        result = pd.merge(user_summary, df_signup[['name', 'email', '_id']], left_on='user_id', right_on='_id')
        result = result[['name', 'email', 'total_items_purchased', 'total_purchase_amount', 'discount_codes', 'total_discount_amount']]
        analysis_json = result.to_dict(orient='records')

        return {'data': analysis_json}, 200
