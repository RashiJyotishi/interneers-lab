from mongoengine import Document, StringField, FloatField, IntField, ReferenceField
from django_app.adapters.repositories.mongo_models.product_category_document import ProductCategoryDocument

class ProductDocument(Document):
    name = StringField(required=True, max_length=200)
    description = StringField(max_length=1000)
    category = ReferenceField(ProductCategoryDocument, null=True)
    price = FloatField(required=True, min_value=0)
    brand = StringField(required=True, max_length=100)
    quantity = IntField(required=True, min_value=0)

    meta = {
        'collection': 'products'
    }