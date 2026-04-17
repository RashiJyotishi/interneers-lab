from django_app.core.models.product import Product
from django_app.adapters.repositories.mongo_models.product_document import ProductDocument
from typing import Optional
from bson import ObjectId
from bson.errors import InvalidId

class MongoProductRepository:

    def _to_domain(self, doc: ProductDocument) -> Product:
        """Convert a DB document → core domain model"""
        # print('MongoProductRepository._to_domain doc.category:', doc.category)

        category_title = ''
        if doc.category:
            category_title = getattr(doc.category, 'title', '')

        return Product(
            id=str(doc.id),
            name=doc.name,
            description=doc.description or '',
            category=category_title,
            price=doc.price,
            brand=doc.brand or '',
            quantity=doc.quantity,
            category_id=str(doc.category.id) if doc.category else None,
        )

    def _to_object_id(self, product_id: str):
        """Safely convert string → ObjectId, return None if invalid"""
        try:
            return ObjectId(product_id)
        except (InvalidId, TypeError):
            return None

    def save(self, product: Product) -> Product:
        from django_app.adapters.repositories.mongo_models.product_category_document import ProductCategoryDocument
        from bson import ObjectId

        category_doc = None
        if product.category_id:
            category_doc = ProductCategoryDocument.objects(
                id=ObjectId(product.category_id)
            ).first()

        if product.id:
            oid = self._to_object_id(product.id)
            doc = ProductDocument.objects(id=oid).first()
            if doc:
                doc.name = product.name
                doc.description = product.description
                # doc.category = product.category
                doc.price = product.price
                doc.brand = product.brand
                doc.quantity = product.quantity
                doc.category = category_doc
                doc.save()
                return self._to_domain(doc)

        # Create new
        doc = ProductDocument(
            name=product.name,
            description=product.description,
            # category=product.category,
            price=product.price,
            brand=product.brand,
            quantity=product.quantity,
            category=category_doc,
        )
        doc.save()
        return self._to_domain(doc)

    def find_by_category(self, category_id: str) -> list[Product]:
        from django_app.adapters.repositories.mongo_models.product_category_document import ProductCategoryDocument
        oid = self._to_object_id(category_id)
        if not oid:
            return []
        category_doc = ProductCategoryDocument.objects(id=oid).first()
        if not category_doc:
            return []
        docs = ProductDocument.objects(category=category_doc)
        return [self._to_domain(doc) for doc in docs]

    def find_by_id(self, product_id: str) -> Optional[Product]:
        doc = ProductDocument.objects(id=product_id).first()
        if not doc:
            return None
        return self._to_domain(doc)

    def find_all(self) -> list[Product]:
        return [self._to_domain(doc) for doc in ProductDocument.objects.all()]

    def delete(self, product_id: str) -> bool:
        doc = ProductDocument.objects(id=product_id).first()
        if not doc:
            return False
        doc.delete()
        return True