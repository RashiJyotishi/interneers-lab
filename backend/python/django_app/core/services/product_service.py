from django_app.core.models.product import Product
from typing import Optional

class ProductService:
    def __init__(self, repository, category_repository=None):
        self.repository = repository  # injected — could be in-memory or mongo
        self.category_repository = category_repository

    def create_product(self, data: dict) -> Product:
        self._validate(data)

        category_id = data.get('category_id')
        if category_id and self.category_repository:
            category = self.category_repository.find_by_id(category_id)
            if not category:
                raise ValueError({'category_id': 'Category not found'})

        product = Product(
            name=data['name'],
            description=data.get('description', ''),
            category=data.get('category', ''),
            price=data['price'],
            brand=data.get('brand'),
            quantity=data['quantity'],
            category_id=category_id,
        )
        return self.repository.save(product)

    def get_products_by_category(self, category_id: str) -> list[Product]:
        return self.repository.find_by_category(category_id)

    def assign_category(self, product_id: str, category_id: str) -> Optional[Product]:
        product = self.repository.find_by_id(product_id)
        if not product:
            return None
        if self.category_repository:
            category = self.category_repository.find_by_id(category_id)
            if not category:
                raise ValueError({'category_id': 'Category not found'})
        product.category_id = category_id
        return self.repository.save(product)

    def remove_category(self, product_id: str) -> Optional[Product]:
        product = self.repository.find_by_id(product_id)
        if not product:
            return None
        product.category_id = None
        return self.repository.save(product)

    def bulk_create_from_csv(self, csv_content: str) -> list[Product]:
        import csv, io
        reader = csv.DictReader(io.StringIO(csv_content))
        created = []
        errors = []

        for i, row in enumerate(reader):
            try:
                # CSV values are always strings — cast types explicitly
                row['price'] = float(row['price'])
                row['quantity'] = int(row['quantity'])
                product = self.create_product(row)
                created.append(product)
            except (ValueError, KeyError) as e:
                errors.append({'row': i + 2, 'error': str(e)})  # +2 for header + 0-index

        if errors:
            raise ValueError(errors)
        return created

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
        if not data.get('brand'):
            errors['brand'] = 'Brand is required'
        if data.get('price') is not None and data['price'] <= 0:
            errors['price'] = 'Price must be greater than 0'
        if data.get('quantity') is not None and data['quantity'] < 0:
            errors['quantity'] = 'Quantity cannot be negative'
        if errors:
            raise ValueError(errors)