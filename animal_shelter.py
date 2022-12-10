from pymongo import MongoClient
from bson.objectid import ObjectId
from pymongo.errors import ConnectionFailure


def update(key, value):
    for i in range(1):
        key = "animal_type"
        value = "Dog"
        return True
    else:
        return False


class AnimalShelter(object):
    """ CRUD operations for animals collection"""

    def __init__(self, username, password):
        # Initializing the MongoClient. This helps to 
        # access the MongoDB databases and collections. 
        self.client = MongoClient('mongodb://%s:%s@localhost:27017/' % (username, password))
        self.database = self.client['AAC']

    def create(self, data):
        if data is not None:
            self.database.animals.insert(data)  # data should be dictionary
            return True
        else:
            raise Exception("Nothing to save, because data parameter is empty")
            return False

    def read(self, data=None):
        if data is not None:
            data = self.database.animals.find(data, {"_id": False})
        else:
            data = self.database.animals.find({}, {"_id": False})
        return data

    def readAll(self, data):
        data_read = self.database.animals.find(data, {"_id": False})
        return data_read

    def delete(self, data):
        if data is not None:
            self.database.animals.delete_one(data)
            return True
        else:
            raise Exception("Nothing to delete because data parameter is invalid")
