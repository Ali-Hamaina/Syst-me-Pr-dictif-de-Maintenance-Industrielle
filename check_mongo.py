from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
collection = client["maintenance"]["predictions"]

print("📦 Contenu de la collection 'predictions':\n")
for doc in collection.find().sort("_id", -1).limit(10):
    print(doc)
