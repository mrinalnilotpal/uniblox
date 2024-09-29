
from .base_api import BaseAPI

class CheckoutAPI(BaseAPI):
    """API to handle the checkout process."""
    def post(self):
        payload = self.get_payload()
        nth_order = self.kwargs.get('nth_order', 1)
        # Checkout logic using nth_order
        return self.response(f"Order placed successfully. This is your {nth_order}th order.")
