# pymongo.py
# Simple PyMongo helper functions for the assignment

from pymongo import MongoClient, ReturnDocument
from bson import ObjectId
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://webuser:WebPass!789@localhost:27017/classdb?authSource=classdb")

def get_client(uri: str = MONGO_URI) -> MongoClient:
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")  # checking if the DB is reachable
    return client

def create_user(db, user_doc):
    """Insert a new user document and return the inserted id as a string."""
    res = db.users.insert_one(user_doc)
    return str(res.inserted_id)

def get_users(db, filter=None, projection=None):
    filter = filter or {}
    cursor = db.users.find(filter, projection)
    results = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])  
        results.append(doc)
    return results

def get_user_by_id(db, id_str):
    try:
        oid = ObjectId(id_str)
    except Exception:
        raise ValueError("Invalid id format")
    doc = db.users.find_one({"_id": oid})
    if doc:
        doc["_id"] = str(doc["_id"])
    return doc

def update_user(db, id_str, update_ops):
    try:
        oid = ObjectId(id_str)
    except Exception:
        raise ValueError("Invalid id format")

    updated = db.users.find_one_and_update(
        {"_id": oid},
        update_ops,
        return_document=ReturnDocument.AFTER
    )
    if updated:
        updated["_id"] = str(updated["_id"])
    return updated

# a brief example when running the file 
if __name__ == "__main__":
    client = get_client()
    db = client.get_database()  
    print("Users now:", get_users(db))
    new_id = create_user(db, {
        "username": "leila",
        "email": "leila@school.edu",
        "profile": {"first_name": "Leila", "last_name": "N.", "age": 22},
        "roles": ["student"]
    })
    print("Inserted id:", new_id)
    upd = update_user(db, new_id, {"$set": {"profile.age": 23}})
    print("After update:", upd)
