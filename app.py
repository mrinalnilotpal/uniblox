import os
import json
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask.helpers import get_root_path

import sys
PATH=sys.path[0]
sys.path.append(PATH)

from web.addtocart import AddToCartAPI
from web.add_product_to_universe import AddProductAPI
from web.analytics import GenerateAnalysisAPI
from web.login import LoginAPI
from web.signup import SignupAPI
from web.checkout import CheckoutAPI


class MyFlask(Flask):
    def __init__(self, *args, **kwargs):
        """
        Custom Flask class to initialize the application and store global variables.
        """
        super().__init__(*args, **kwargs)
        self.global_variables = {}

    def from_local_config(self, local_config):
        """
        Load the configuration data from a JSON file and set necessary parameters.
        """
        with open(local_config) as json_file:
            config_data = json.load(json_file)

            self.DISCOUNT_PERCENTAGE = config_data["DISCOUNT"]["percentage"]
            self.NTH_ORDER = config_data["DISCOUNT"]["nth_order"]
            self.SIGNUP_DB = config_data["SIGNUP_DB"]
            self.PRODUCT_DB = config_data["PRODUCT_DB"]
            self.ORDER_DB = config_data["ORDER_DB"]

    def add_api(self):
        """
        Add API routes to the Flask application and bind them to specific endpoints.
        """
        api = Api(self, catch_all_404s=True)

        api.add_resource(
            AddToCartAPI,
            "/api/v1/cart/add",
            endpoint="add_to_cart",
            resource_class_kwargs={
                "signup_db": self.SIGNUP_DB,
            },
        )

        api.add_resource(
            CheckoutAPI,
            "/api/v1/checkout",
            endpoint="checkout",
            resource_class_kwargs={
                "nth_order": self.NTH_ORDER,
                "product_db":self.PRODUCT_DB,
                "signup_db":self.SIGNUP_DB,
                "orders_db" : self.ORDER_DB
            },
        )

        api.add_resource(
            GenerateAnalysisAPI,
            "/api/v1/admin/analysis",
            endpoint="analysis",
            resource_class_kwargs={
                "product_db":self.PRODUCT_DB,
                "signup_db":self.SIGNUP_DB,
                "orders_db" : self.ORDER_DB
            },
        )

        api.add_resource(
            LoginAPI,
            "/api/v1/auth/login",
            endpoint="login",
            resource_class_kwargs={
                "signup_db": self.SIGNUP_DB,
            },
        )

        api.add_resource(
            SignupAPI,
            "/api/v1/auth/signup",
            endpoint="signup",
            resource_class_kwargs={
                "signup_db": self.SIGNUP_DB,
            },
        )

        api.add_resource(
            AddProductAPI,
            "/api/v1/product/add",
            endpoint="add_product",
            resource_class_kwargs={
                "product_db": self.PRODUCT_DB,
            },
        )


def create_app(config_file):
    """
    Factory function to create a Flask application instance.
    Loads configurations from a JSON file and adds API routes.
    """
    app = MyFlask(__name__)
    CORS(app)
    ROOT = get_root_path("app")
    print(ROOT)
    LOCAL_CONFIG = os.path.join(ROOT, config_file)
    print(LOCAL_CONFIG)
    app.from_local_config(LOCAL_CONFIG)
    app.add_api()
    return app


app = create_app(config_file="local_config.json")


if __name__ == "__main__":
    """
    Main entry point to run the Flask application in debug mode.
    """
    app.run(
        debug=True
    )
