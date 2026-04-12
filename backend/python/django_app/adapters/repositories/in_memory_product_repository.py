from django_app.core.models.product import Product
from typing import Optional

class InMemoryProductRepository:
    def __init__(self):
        self._store = {}  # our "database"

    def save(self, product: Product) -> Product:
        self._store[product.id] = product
        return product

    def find_by_id(self, product_id: str) -> Optional[Product]:
        return self._store.get(product_id)

    def find_all(self) -> list[Product]:
        return list(self._store.values())

    def delete(self, product_id: str) -> bool:
        if product_id in self._store:
            del self._store[product_id]
            return True
        return False