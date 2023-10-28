from src.server.server import ProtocolTypeRouter, HttpServer, WebSocketServer
from src.server.route import Route, WebSocketRoute

from src.model.data_adapter import DataAdapter

import json
from src.model.user import User
from src.model.shift import Shift
from src.algorithms.Solvers import SASolver, DAUSolver
import time

mongodbDataAdapter = DataAdapter()

class GetUser(Route):

    def handle(self):
        if self.request.method == 'POST':
            body = json.loads(self.request.body)
            username = body['username']
            password = body['password']
            user = mongodbDataAdapter.getUser(username, password)
            self.response.send(200, user.toJson(), content_type='application/json')
        else:
            self.response.send(400, 'Bad Request')

class UpdateUserShifts(Route):

    def handle(self):
        if self.request.method == 'POST':
            body = json.loads(self.request.body)
            user = User(**body)
            mongodbDataAdapter.updateUserShifts(user)
            self.response.send(200, 'Finish')
        else:
            self.response.send(400, 'Bad Request')

class SaveShift(Route):

    def handle(self):
        if self.request.method == 'POST':
            body = json.loads(self.request.body)
            user = User(**body['user'])
            shift = Shift(body['shift'])         
            mongodbDataAdapter.saveShift(user, shift)
            self.response.send(200, 'Finish')
        else:
            self.response.send(400, 'Bad Request')

class LoadShift(Route):

    def handle(self):
        if self.request.method == 'POST':
            body = json.loads(self.request.body)
            shift_id = body['shift_id']
            shift = mongodbDataAdapter.loadShift(shift_id)
            data_json = shift.toJson()
            self.response.send(200, data_json, content_type='application/json')
        else:
            self.response.send(400, 'Bad Request')

class LoadShifts(Route):

    def handle(self):
        shifts_list = {'shifts_list':[]}
        if self.request.method == 'POST':
            body = json.loads(self.request.body)
            user = User(**body['user'])       
            shifts=mongodbDataAdapter.loadShifts(user)
            for i in range(len(shifts)):
                data_json = shifts[i].toJson()
                shifts_list['shifts_list'].append(data_json)
            self.response.send(200, json.dumps(shifts_list), content_type='application/json')
        else:
            self.response.send(400, 'Bad Request')


class SolverWebsocketRoute(WebSocketRoute):

    def __init__(self, request, response, solver_type):
        super().__init__(request, response)
        self.solver_type = solver_type

    def handle(self):
        while True:
            received_message = self._recv()
            if received_message is None:
                break
            else:
                self.response.send("Received")
            problem = json.loads(received_message)
            solver = self.solver_type(problem)
            self.response.send("Compiling...")
            solver.compile()
            self.response.send("Finish compiling")
            shifts = solver.solve()
            result = json.dumps(shifts, default=lambda o: o.__dict__, indent=4)
            self.response.send(result)
            self.response.send("Finish solving")
            
        pass

class DAUWebsocketRoute(SolverWebsocketRoute):

    def __init__(self, request, response):
        super().__init__(request, response, DAUSolver)

class SAWebsocketRoute(SolverWebsocketRoute):

    def __init__(self, request, response):
        super().__init__(request, response, SASolver)



if __name__ == '__main__':
    server = ProtocolTypeRouter({
        'http': HttpServer(routes=[
            (r'/user', GetUser), (r'/updateusershifts', UpdateUserShifts), 
            (r'/saveshift', SaveShift), (r'/loadshift$', LoadShift), 
            (r'/loadshifts$', LoadShifts)
        ]),
        'websocket': WebSocketServer(routes=[
                (r'/dau', DAUWebsocketRoute),
                (r'/sa', SAWebsocketRoute)
            ])
        })
    server.run()