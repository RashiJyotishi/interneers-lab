from mongoengine import Document, StringField

class ProductCategoryDocument(Document):
    title = StringField(required=True, max_length=100)
    description = StringField(max_length=500)

    meta = {'collection': 'product_categories'}