import os
import sys
from pathlib import Path
from pymongo import MongoClient

# 1. Path Setup
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_app.settings')

# 2. Connection details (Auth ke saath)
# Apne settings.py se credentials verify kar lena
# MONGO_USER = "root"
# MONGO_PASS = "example"

client = MongoClient(
    host='localhost',
    port=27017,
    # username=MONGO_USER,
    # password=MONGO_PASS,
    # authSource='admin'
)

db = client['interneers_lab_2026_mongodb']
collection = db['products']

# 3. Pehle check karte hain ki kya humein wo "Electronics" wala product mil raha hai
print("DEBUG: Checking for products with string category...")
sample = collection.find_one({'category': 'Electronics'})

if sample:
    print(f"FOUND: Product '{sample.get('name')}' has a string category. Fixing now...")

    # Sabhi products jahan category "Electronics" ya koi aur string hai, unhe null karo
    result = collection.update_many(
        { 'category': { '$type': 'string' } },
        { '$set': { 'category': None } }
    )
    print(f"SUCCESS: Fixed {result.modified_count} products.")
else:
    print("NOT FOUND: No product found with category='Electronics'.")
    print("Checking for ANY product that doesn't have a null/DBRef category...")

    # Ek aur try: Har wo cheez jo null nahi hai aur object nahi hai (string check)
    all_docs = collection.find()
    count = 0
    for doc in all_docs:
        cat = doc.get('category')
        if cat and isinstance(cat, str):
            collection.update_one({'_id': doc['_id']}, {'$set': {'category': None}})
            count += 1
    print(f"Manual Loop Fix: Fixed {count} products.")

client.close()