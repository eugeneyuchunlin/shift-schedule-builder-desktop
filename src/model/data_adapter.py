from .user import User
from .shift import Shift

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from src.model import MONGODB_URI
import pandas as pd

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

        user = User(username=user_data['username'], password=user_data['password'], email=user_data['email'], shifts=user_data['shifts'])
        return user
    
    def updateUserShifts(self, user:User):
        user_collection = self.db.Users
        user_collection.update_one({"username": user.getUsername()}, {"$set": {"shifts": user.getShifts()}})
        pass

    def saveShift(self, user:User, shift:Shift):
        # write your code here
        # you can refer _solver.py DAUSolver.saveShift()
        # save the result

        collection = self.db.Shifts
        tables = shift.getTables()


        inserted_data = shift.getShiftConfiguration() 
        inserted_data['table'] = tables
        collection.update_one({"shift_id" : shift.getShiftId()}, {"$set": inserted_data}, upsert=True)

        user.addShift(shift.getShiftId())
        self.updateUserShifts(user)
    
    def loadShift(self, shift_id) -> Shift:
        shift = self.db.Shifts.find_one({"shift_id": shift_id})

        tables = shift['table']
        del shift['table']

        shift = Shift(shift_id=shift['shift_id'], shift_configuration=shift, tables=tables)

        return shift

    def loadShifts(self, user:User):
        # write your code here
        shifts = []

        for shift_id in user.getShifts():
            shift_df = self.loadShift(shift_id)    
            shifts.append(shift_df)

        return shifts

