from .user import User

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from src.model import MONGODB_URI

db_client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))
try:
    db_client.admin.command("ping")
    print("Connected to MongoDB")
except Exception as e:
    print("Unable to connect to MongoDB")
    print(e)




class DataAdapter(object):

    def __init__(self):
        self.db = db_client["Test1"]

    def getUser(self, username, password):
        user_data = self.db.Users.find_one({"username": username, "password": password})
        if user_data is None:
            return

        user = User(username=user_data['username'], password=user_data['password'], email=user_data['email'], shifts=[])
        return user

    def saveShift(self, user:User, shifts:[], scores:[]):
        # write your code here
        # you can refer _solver.py DAUSolver.saveShift()
        # save the result
        pass