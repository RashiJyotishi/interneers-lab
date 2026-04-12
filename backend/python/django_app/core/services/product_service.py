from django_app.core.models.product import Product
from typing import Optional

class ProductService:
    def __init__(self, repository):
        self.repository = repository  # injected — could be in-memory or mongo

    def create_product(self, data: dict) -> Product:
        self._validate(data)
        product = Product(
            name=data['name'],
            description=data.get('description', ''),
            category=data.get('category', ''),
            price=data['price'],
            brand=data.get('brand', ''),
            quantity=data['quantity'],
        )
        return self.repository.save(product)

    def get_product(self, product_id: str) -> Optional[Product]:
        return self.repository.find_by_id(product_id)

    def get_all_products(self) -> list[Product]:
        return self.repository.find_all()

    def update_product(self, product_id: str, data: dict) -> Optional[Product]:
        product = self.repository.find_by_id(product_id)
        if not product:
            return None
        self._validate(data)
        product.name = data.get('name', product.name)
        product.price = data.get('price', product.price)
        product.quantity = data.get('quantity', product.quantity)
        product.description = data.get('description', product.description)
        product.category = data.get('category', product.category)
        product.brand = data.get('brand', product.brand)
        return self.repository.save(product)

    def delete_product(self, product_id: str) -> bool:
        return self.repository.delete(product_id)

    def _validate(self, data: dict):
        errors = {}
        if not data.get('name'):
            errors['name'] = 'Name is required'
        if data.get('price') is not None and data['price'] <= 0:
            errors['price'] = 'Price must be greater than 0'
        if data.get('quantity') is not None and data['quantity'] < 0:
            errors['quantity'] = 'Quantity cannot be negative'
        if errors:
            raise ValueError(errors)