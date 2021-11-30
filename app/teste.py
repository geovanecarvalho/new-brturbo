from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017/")

db = client["db"]
collection = db["user"]


# collection.update_one({"db": "user"}, {"name": "tiago"})

collection.update_one({"name": "geovane"}, {"$set": {"name": "Fernando"}})
