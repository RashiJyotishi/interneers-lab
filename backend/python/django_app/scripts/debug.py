# debug_db.py
from pymongo import MongoClient

client = MongoClient('localhost', 27017)

# 1. Saare database names print karo
print(f"Available Databases: {client.list_database_names()}")

# 2. Django settings waale DB mein ghuso
db = client['interneers_lab_2026_mongodb']
print(f"Collections in this DB: {db.list_collection_names()}")

# 3. Agar 'products' collection hai, toh pehla document dekho
if 'products' in db.list_collection_names():
    first_doc = db.products.find_one()
    print(f"First document in 'products': {first_doc}")
else:
    print("FATAL: 'products' collection NOT FOUND in this database!")

client.close()