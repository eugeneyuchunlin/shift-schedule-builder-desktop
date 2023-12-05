# define user class here
# username: str, 
# password: str, 
# email: str, 
# shifts: []
import json

class User(object):

    def __init__(self, **kwargs):
        self.username = kwargs.get('username', "")
        self.password = kwargs.get('password', "")
        self.email = kwargs.get('email', "")
        self.shifts = kwargs.get('shifts', [])

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
        
    def data(self):
        return {
            'username' : self.username,
            'password' : self.password,
            'email' : self.email,
            'shifts': self.shifts
        }

    def toJson(self):
        return json.dumps(self.data(), indent=4)