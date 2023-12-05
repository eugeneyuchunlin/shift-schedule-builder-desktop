#mongoDB collection name:Registries
#document
#FS:"1"
#OSC:"0"
import json

class Registry(object):

    def __init__(self, **kwargs):
        self.service = kwargs['service']
        self.status = kwargs['status']

    def getService(self):
        return self.service

    def getStatus(self):
        return self.status

    def setService(self, service):
        if(type(service) != str):
            raise Exception("TypeError")
        self.service = service

    def setStatus(self, status):
        if(type(status) != str):
            raise Exception("TypeError")
        self.status = status
        
    def data(self):
        return {
            'service' : self.service,
            'status' : self.status,
        }

    def toJson(self):
        return json.dumps(self.data(), indent=2)