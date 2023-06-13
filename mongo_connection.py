from pymongo import MongoClient

def get_mongo_collection():
    
    client = MongoClient('mongodb', 27017)
    database = client["pruebasAutomatizadas"]

    collection_name = "pruebas"
    collection = database[collection_name]

    return collection