from .user import User

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

MONGODB_URI = ""
db_client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))
try:
    db_client.admin.command("ping")
    print("Connected to MongoDB")
except Exception as e:
    print("Unable to connect to MongoDB")
    print(e)




class DataAdapter(object):

    def __init__(self):
        self.db = db_client["test"]

    def getUser(self, username, password):
        user = self.db.users.find_one({"username": username, "password": password}) 
        
        # write your code here
        # return a User object

    def saveShift(self, user:User, shifts:[], scores:[]):
        # write your code here
        # you can refer _solver.py DAUSolver.saveShift()
        # save the result
        pass