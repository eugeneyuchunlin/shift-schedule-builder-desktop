from .user import User
from .shift import Shift
from .registry import Registry

import redis
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from src.model import MONGODB_URI
import pandas as pd
import json
import requests
from requests.adapters import HTTPAdapter

redis_client = redis.StrictRedis(
                    host='redis-12297.c302.asia-northeast1-1.gce.cloud.redislabs.com',
                    port=12297,
                    password='W1m4qxXnWu0waZpAJqiWcWgmQFVKzejX'
                )

db_client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))
try:
    db_client.admin.command("ping")
    # print("Connected to MongoDB")
except Exception as e:
    print("Unable to connect to MongoDB")
    print(e)


class DataAccess(object):

    def __init__(self, db_name:str):
        self.db = db_client[db_name]

    def getUser(self, username:str, password:str):
        pass

    def updateUserShifts(self, user:User):
        pass

    def saveShift(self, user:User, shift:Shift):
        pass

    def loadShift(self, shift_id:str) -> Shift:
        pass

    def loadShifts(self, user:User):
        pass

class DataAdapter(DataAccess):

    def __init__(self):
        super().__init__("Test1")

    def getUser(self, username:str, password:str):
        redis_key = f"{username}{password}"
        json_data = redis_client.execute_command('JSON.GET', redis_key)
        user_data = json.loads(json_data)
        #user_data = self.db.Users.find_one({"username": username, "password": password})
        if user_data is None:
            return

        user = User(**user_data)
        return user
    
    def updateUserShifts(self, user:User):
        redis_key = f"{user.getUsername()}{user.getPassword()}"
        json_data = redis_client.execute_command('JSON.GET', redis_key)
        user_data = json.loads(json_data)
        user_data["shifts"] = user.getShifts()
        updated_json_data = json.dumps(user_data)
        redis_client.execute_command('JSON.SET', redis_key, '.', updated_json_data)

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
    
    def loadShift(self, shift_id:str) -> Shift:
        shift = self.db.Shifts.find_one({"shift_id": shift_id})
        del shift['_id']
        shift = Shift(shift)
        return shift

    def loadShifts(self, user:User):
        # write your code here
        shifts = []  
        for shift_id in user.getShifts():
            shift_df = self.loadShift(shift_id)    
            shifts.append(shift_df.getShiftConfiguration())
        return shifts

    def addRegistry(self, registry:Registry):
        registry_collection = self.db.Registries
        registry_collection.update_one({}, {"$set": {"FS": registry.getFS()}})
        registry_collection.update_one({}, {"$set": {"OSC": registry.getOSC()}})
        pass

    #def getHealthCheck(self, fs_status:str, osc_status:str):
    #    registries_status = self.db.Registries.find_one({"FS": fs_status, "OSC": osc_status})
    #    if registries_status is None:
    #        return
    #    registry = Registry(**registries_status)
    #    return registry
    def getHealthCheck(self):
        registries_status = self.db.Registries.find_one()
        registry = Registry(**registries_status)
        return registry

class RemoteDataAdapter(DataAccess):

    def __init__(self):
        super().__init__("Test1")

    def getUser(self, username:str, password:str):
        r = requests.post("http://localhost:8888/user", json={"username":username, "password":password})
        user_data = json.loads(r.text)
        user = User(**user_data)
        return user

    def updateUserShifts(self, user:User):
        r = requests.post("http://localhost:8888/updateusershifts", json=user.data())
        return r.text

    def saveShift(self, user:User, shift:Shift):
        r = requests.post("http://localhost:8888/saveshifts", json={'user' : user.data(), 'shift': shift.getShiftConfiguration()})
        return r.text

    def loadShift(self, shift_id:str) -> Shift:
        r = requests.post("http://localhost:8888/loadshift", json={"shift_id":shift_id})
        shift_data = json.loads(r.text)
        print(shift_data)
        shift = Shift(shift_data)
        return shift

    def loadShifts(self, user:User):
        r = requests.post("http://localhost:8888/loadshifts", json=user.data())
        shifts_data = json.loads(r.text)
        return json.dumps(shifts_data)
