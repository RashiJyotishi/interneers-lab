from mongoengine import Document, StringField, FloatField, IntField

class ProductDocument(Document):
    name = StringField(required=True, max_length=200)
    description = StringField(max_length=1000)
    category = StringField(max_length=100)
    price = FloatField(required=True, min_value=0)
    brand = StringField(max_length=100)
    quantity = IntField(required=True, min_value=0)

    meta = {
        'collection': 'products'
    }