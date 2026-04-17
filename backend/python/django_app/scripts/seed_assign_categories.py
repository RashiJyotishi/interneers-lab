# scripts/seed_assign_categories.py
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_app.settings')
django.setup()

from django_app.adapters.repositories.mongo_models.product_document import ProductDocument
from django_app.adapters.repositories.mongo_models.product_category_document import ProductCategoryDocument

# Fetch all categories into a dict by title for easy lookup
categories = {doc.title: doc for doc in ProductCategoryDocument.objects.all()}
print("Found categories:", list(categories.keys()))

# Define which product names map to which category
# Adjust these to match whatever products you have in your DB
assignments = {
    "Mechanical Keyboard": "Electronics",
    "Wireless Mouse":      "Electronics",
    "USB Hub":             "Electronics",
    # add more here as needed
}

for product_name, category_title in assignments.items():
    product = ProductDocument.objects(name=product_name).first()
    category = categories.get(category_title)

    if not product:
        print(f"⚠️  Product not found: '{product_name}' — skipping")
        continue
    if not category:
        print(f"⚠️  Category not found: '{category_title}' — skipping")
        continue

    product.category = category
    product.save()
    print(f"✅ Assigned '{product_name}' → '{category_title}'")

print("\nDone! Check Compass to verify the category DBRefs are set.")