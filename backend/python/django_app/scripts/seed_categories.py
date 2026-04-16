# scripts/seed_categories.py
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_app.settings')
django.setup()

from django_app.adapters.repositories.mongo_models.product_category_document import ProductCategoryDocument

# Clear existing categories first to avoid duplicates on re-run
ProductCategoryDocument.objects.delete()
print("Cleared existing categories")

categories = [
    {
        "title": "Electronics",
        "description": "Electronic devices and accessories like keyboards, mice, and hubs"
    },
    {
        "title": "Food",
        "description": "Edible products including snacks, beverages and pantry staples"
    },
    {
        "title": "Kitchen Essentials",
        "description": "Cookware, utensils and appliances for the kitchen"
    },
    {
        "title": "Stationery",
        "description": "Office and school supplies like pens, notebooks and folders"
    },
]

created = []
for cat in categories:
    doc = ProductCategoryDocument(
        title=cat["title"],
        description=cat["description"]
    )
    doc.save()
    created.append(doc)
    print(f"Created category: '{doc.title}' with id: {doc.id}")

print(f"\n✅ Seeded {len(created)} categories successfully")
print("\nCopy these IDs for Postman testing:")
for doc in created:
    print(f"  {doc.title}: {doc.id}")