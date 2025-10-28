# mongoengine.py
from mongoengine import (
    connect, Document, EmbeddedDocument, StringField, IntField,
    EmbeddedDocumentField, ListField, DateTimeField, EmailField
)
from datetime import datetime
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://webuser:WebPass!789@localhost:27017/classdb?authSource=classdb")

def init_connection(uri=MONGO_URI):
    connect(host=uri)

class Address(EmbeddedDocument):
    street = StringField()
    city = StringField()
    country = StringField()

class Profile(EmbeddedDocument):
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    age = IntField()
    addresses = ListField(EmbeddedDocumentField(Address))

class Student(Document):
    meta = {"collection": "users"}  # we reuse the same collection name
    username = StringField(required=True, unique=True)
    email = EmailField(required=True, unique=True)
    profile = EmbeddedDocumentField(Profile)
    roles = ListField(StringField())
    created_at = DateTimeField(default=datetime.utcnow)

def create_student(data: dict) -> Student:
    s = Student(**data)
    s.save()
    return s

def find_students(filter=None) -> list:
    filter = filter or {}
    qs = Student.objects.filter(**filter)
    return list(qs)

def update_student_by_username(username: str, updates: dict) -> Student:
    # updates example: {"set__profile__age": 24}
    return Student.objects(username=username).modify(new=True, **updates)

if __name__ == "__main__":
    init_connection()
    # example create
    s = create_student({
        "username": "nora",
        "email": "nora@uni.edu",
        "profile": {
            "first_name": "Nora",
            "last_name": "K",
            "age": 24,
            "addresses": [{"street": "20 Elm St", "city": "Lyon", "country": "FR"}]
        },
        "roles": ["student"]
    })
    print("Created:", s.id)
    found = find_students({"profile__age__gte": 23})
    print("Found count:", len(found))
