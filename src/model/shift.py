import pandas as pd
import json

class Shift(object):

    def __init__(self, shift_configuration):
        self.shift_id = shift_configuration['shift_id']
        self.shift_configuration = shift_configuration
        self.tables = shift_configuration['table']
        
    def getShiftId(self):
        return self.shift_id
    
    def getShiftConfiguration(self):
        return self.shift_configuration
    
    def getShift(self, index=0):
        table = self.tables[index]
        # prepare the dataframe 

        df = pd.DataFrame(table, columns=[str(i) for i in range(1, len(table[0]) + 1)])
        # insert the name list to the dataframe at col 0
        df.insert(0, "name", self.shift_configuration['name_list'])
        return df
    
    def setShiftId(self, shift_id):
        if(type(shift_id) != str):
            raise Exception("TypeError")
        self.shift_id = shift_id

    def setParameters(self, parameters):
        if(type(parameters) != dict):
            raise Exception("TypeError")
        self.parameters = parameters

    def setTables(self, tables):
        self.tables = tables

    def getTables(self):
        return self.tables
    
    def toJson(self):
        data = self.shift_configuration
        return json.dumps(data)

    