#mongoDB collection name:Registries
#document
#FS:"1"
#OSC:"0"
import json

class Registry(object):

    def __init__(self, **kwargs):
        self.fs_status = kwargs['FS']
        self.osc_status = kwargs['OSC']

    def getFS(self):
        return self.fs_status

    def getOSC(self):
        return self.osc_status

    def setFS(self, fs_status):
        if(type(fs_status) != str):
            raise Exception("TypeError")
        self.fs_status = fs_status

    def setOSC(self, osc_status):
        if(type(osc_status) != str):
            raise Exception("TypeError")
        self.password = osc_status
        
    def data(self):
        return {
            'FS' : self.fs_status,
            'OSC' : self.osc_status,
        }

    def toJson(self):
        return json.dumps(self.data(), indent=2)