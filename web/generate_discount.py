# api/discount_api.py

from .base_api import BaseAPI, admin_required

class GenerateDiscountAPI(BaseAPI):
    """API to generate a discount for admin users."""
    @admin_required
    def post(self):
        discount_percentage = self.kwargs.get('discount_percentage', 0)
        nth_order = self.kwargs.get('nth_order', 1)
        # Logic to generate discount
        return self.response(f"Generated a {discount_percentage}% discount for the {nth_order}th order.")
