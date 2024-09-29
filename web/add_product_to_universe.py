from .base_api import BaseAPI, admin_required

class AddProductAPI(BaseAPI):
    """API to add a new product (admin-only)."""
    @admin_required
    def post(self):
        payload = self.get_payload()
        # Logic to add product
        return self.response(f"Product {payload.get('name')} added successfully.")