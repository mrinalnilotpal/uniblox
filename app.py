import os
import json
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask.helpers import get_root_path

from web import (
    AddToCartAPI,
    CheckoutAPI,
    GenerateDiscountAPI,
    AdminStatsAPI,
    LoginAPI,
    SignupAPI,
    AddProductAPI,
)

class MyFlask(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.global_variables = {}

    def from_local_config(self, local_config):
        with open(local_config) as json_file:
            config_data = json.load(json_file)

            self.DISCOUNT_PERCENTAGE = config_data["DISCOUNT"]["percentage"]
            self.NTH_ORDER = config_data["DISCOUNT"]["nth_order"]

    def add_api(self):
        api = Api(self, catch_all_404s=True)

        api.add_resource(
            AddToCartAPI,
            "/api/v1/cart/add",
            endpoint="add_to_cart",
            resource_class_kwargs={
                "discount_percentage": self.DISCOUNT_PERCENTAGE
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
            endpoint="admin_stats"
        )

        api.add_resource(
            LoginAPI,
            "/api/v1/auth/login",
            endpoint="login"
        )

        api.add_resource(
            SignupAPI,
            "/api/v1/auth/signup",
            endpoint="signup"
        )

        api.add_resource(
            AddProductAPI,
            "/api/v1/product/add",
            endpoint="add_product"
        )


def create_app(config_file):
    app = MyFlask(__name__)
    CORS(app)
    ROOT = get_root_path("app")
    LOCAL_CONFIG = os.path.join(ROOT, config_file)
    app.from_local_config(LOCAL_CONFIG)
    app.add_api()
    return app


app = create_app(config_file="local_config.json")


if __name__ == "__main__":
    app.run(
        debug=True
    )
