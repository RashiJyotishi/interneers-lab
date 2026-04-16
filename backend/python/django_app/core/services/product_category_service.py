# core/services/product_category_service.py
from django_app.core.models.product_category import ProductCategory
from typing import Optional

class ProductCategoryService:
    def __init__(self, repository):
        self.repository = repository

    def create_category(self, data: dict) -> ProductCategory:
        self._validate(data)
        category = ProductCategory(
            title=data['title'],
            description=data.get('description', ''),
        )
        return self.repository.save(category)

    def get_category(self, category_id: str) -> Optional[ProductCategory]:
        return self.repository.find_by_id(category_id)

    def get_all_categories(self) -> list[ProductCategory]:
        return self.repository.find_all()

    def update_category(self, category_id: str, data: dict) -> Optional[ProductCategory]:
        category = self.repository.find_by_id(category_id)
        if not category:
            return None
        self._validate(data)
        category.title = data.get('title', category.title)
        category.description = data.get('description', category.description)
        return self.repository.save(category)

    def delete_category(self, category_id: str) -> bool:
        return self.repository.delete(category_id)

    def _validate(self, data: dict):
        errors = {}
        if not data.get('title'):
            errors['title'] = 'Title is required'
        if errors:
            raise ValueError(errors)