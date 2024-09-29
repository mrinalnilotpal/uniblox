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
from web.generate_discount import GenerateDiscountAPI
from web.login import LoginAPI
from web.signup import SignupAPI
from web.checkout import CheckoutAPI
from web.admin_stats import AdminStatsAPI


class MyFlask(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.global_variables = {}

    def from_local_config(self, local_config):
        with open(local_config) as json_file:
            config_data = json.load(json_file)

            self.DISCOUNT_PERCENTAGE = config_data["DISCOUNT"]["percentage"]
            self.NTH_ORDER = config_data["DISCOUNT"]["nth_order"]
            self.SIGNUP_DB = config_data["SIGNUP_DB"]
            self.PRODUCT_DB = config_data["PRODUCT_DB"]
    def add_api(self):
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
                "nth_order": self.NTH_ORDER
            },
        )

        api.add_resource(
            GenerateDiscountAPI,
            "/api/v1/admin/discount",
            endpoint="generate_discount",
            resource_class_kwargs={
                "nth_order": self.NTH_ORDER,
                "discount_percentage": self.DISCOUNT_PERCENTAGE
            },
        )

        api.add_resource(
            AdminStatsAPI,
            "/api/v1/admin/stats",
            endpoint="admin_stats",
            resource_class_kwargs={
                "product_db": self.PRODUCT_DB,
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
    app.run(
        debug=True
    )
