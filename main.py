import json, yaml, csv, xml.etree.ElementTree as ET
from typing import TypedDict
from collections import namedtuple
from dataclasses import dataclass
from pydantic import BaseModel
import numpy as np
import pandas as pd
import time

# 1. Decorator to measure time
def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time()-start:.5f} sec")
        return result
    return wrapper

# 2. Different data structures
class UserTypedDict(TypedDict):
    id: int
    name: str
    email: str
    age: int

UserNamedTuple = namedtuple("UserNamedTuple", ["id", "name", "email", "age"])

@dataclass
class UserDataClass:
    id: int
    name: str
    email: str
    age: int

class UserModel(BaseModel):
    id: int
    name: str
    email: str
    age: int

# 3. Read files from /data
def read_json(path="data/users.json"):
    with open(path) as f: return json.load(f)

def read_yaml(path="data/users.yaml"):
    with open(path) as f: return yaml.safe_load(f)

def read_csv(path="data/users.csv"):
    with open(path) as f: return list(csv.DictReader(f))

def read_xml(path="data/users.xml"):
    tree = ET.parse(path); root = tree.getroot()
    users = []
    for u in root.findall("user"):
        users.append({
            "id": int(u.find("id").text),
            "name": u.find("name").text,
            "email": u.find("email").text,
            "age": int(u.find("age").text)
        })
    return users

@timer
def list_sum(n=1_000_00):
    return sum([i for i in range(n)])

@timer
def numpy_sum(n=1_000_00):
    return np.sum(np.arange(n))

# 5. Main
def main():
    print("\n--- Reading files ---")
    print("JSON:", read_json())
    print("YAML:", read_yaml())
    print("CSV:", read_csv())
    print("XML:", read_xml())

    print("\n--- Data structures ---")
    user = {"id":1,"name":"Alice","email":"alice@example.com","age":25}
    print("TypedDict:", UserTypedDict(**user))
    print("NamedTuple:", UserNamedTuple(**user))
    print("Dataclass:", UserDataClass(**user))
    print("Pydantic:", UserModel(**user))

    print("\n--- Performance ---")
    list_sum(2000000)
    numpy_sum(2000000)

    print("\n--- Pandas CSV ---")
    df = pd.read_csv("data/users.csv")
    print(df)

if __name__ == "__main__":
    main()
