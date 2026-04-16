# adapters/repositories/mongo_product_category_repository.py
from bson import ObjectId
from bson.errors import InvalidId
from django_app.core.models.product_category import ProductCategory
from django_app.adapters.repositories.mongo_models.product_category_document import ProductCategoryDocument
from typing import Optional

class MongoProductCategoryRepository:

    def _to_domain(self, doc: ProductCategoryDocument) -> ProductCategory:
        return ProductCategory(
            id=str(doc.id),
            title=doc.title,
            description=doc.description or '',
        )

    def _to_object_id(self, category_id: str):
        try:
            return ObjectId(category_id)
        except (InvalidId, TypeError):
            return None

    def save(self, category: ProductCategory) -> ProductCategory:
        if category.id:
            oid = self._to_object_id(category.id)
            doc = ProductCategoryDocument.objects(id=oid).first()
            if doc:
                doc.title = category.title
                doc.description = category.description
                doc.save()
                return self._to_domain(doc)

        doc = ProductCategoryDocument(
            title=category.title,
            description=category.description,
        )
        doc.save()
        return self._to_domain(doc)

    def find_by_id(self, category_id: str) -> Optional[ProductCategory]:
        oid = self._to_object_id(category_id)
        if not oid:
            return None
        doc = ProductCategoryDocument.objects(id=oid).first()
        return self._to_domain(doc) if doc else None

    def find_all(self) -> list[ProductCategory]:
        return [self._to_domain(doc) for doc in ProductCategoryDocument.objects.all()]

    def delete(self, category_id: str) -> bool:
        oid = self._to_object_id(category_id)
        if not oid:
            return False
        doc = ProductCategoryDocument.objects(id=oid).first()
        if not doc:
            return False
        doc.delete()
        return True

