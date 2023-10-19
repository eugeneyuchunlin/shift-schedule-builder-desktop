# define user class here
# username: str, 
# password: str, 
# email: str, 
# shifts: []
import json

class User(object):

    def __init__(self, username, password, email, shifts):
        self.username = username
        self.password = password
        self.email = email
        self.shifts = shifts

    def getUsername(self):
        return self.username

    def getPassword(self):
        return self.password

    def getEmail(self):
        return self.email

    def getShifts(self):
        return self.shifts

    def setUsername(self, username):
        if(type(username) != str):
            raise Exception("TypeError")
        self.username = username

    def setPassword(self, password):
        if(type(password) != str):
            raise Exception("TypeError")
        self.password = password

    def setEmail(self, email):
        if(type(email) != str):
            raise Exception("TypeError")
        self.email = email

    def setShifts(self, shifts):
        if(type(shifts) != list):
            raise Exception("TypeError")
        self.shifts = shifts

    def addShift(self, shift_id):
        if self.shifts.count(shift_id) > 0:
            pass
        else:
            self.shifts.append(shift_id)

    def toJson(self):
        return json.dumps({
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'shifts': self.shifts
        }, indent=4)