from src.server.server import ProtocolTypeRouter, HttpServer, WebSocketServer
from src.server.route import Route, WebSocketRoute

from src.model.data_adapter import DataAdapter

import json
from src.model.user import User
from src.model.shift import Shift
from src.model.registry import Registry
from src.algorithms.Solvers import SASolver, DAUSolver
import time
import requests
from os import path

mongodbDataAdapter = DataAdapter()
redisDataAdapter = DataAdapter()

class Login(Route):

    def handle(self):
        if self.request.method == 'POST':
            body = json.loads(self.request.body)
            username = body['username']
            password = body['password']
            user = mongodbDataAdapter.getUser(username, password)
            if user is None:
                self.response.send(400, json.dumps({"message" : "failed"}), content_type='application/json')
            else:
                data = {
                    "username": user.username,
                    "password" : user.password,
                    "shifts": user.shifts
                }
                self.response.send(200, json.dumps({"message": "successful", "data" : data}), content_type='application/json')
        else:
            self.response.send(400, 'Bad Request')

class GetUser(Route):

    def handle(self):
        if self.request.method == 'POST':
            body = json.loads(self.request.body)
            username = body['username']
            password = body['password']
            #user = mongodbDataAdapter.getUser(username, password)
            user = redisDataAdapter.getUser(username,password)
            self.response.send(200, user.toJson(), content_type='application/json')
        else:
            self.response.send(400, 'Bad Request')

class UpdateUserShifts(Route):

    def handle(self):
        if self.request.method == 'POST':
            body = json.loads(self.request.body)
            user = User(**body)
            #mongodbDataAdapter.updateUserShifts(user)
            redisDataAdapter.updateUserShifts(user)
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
            self.response.send(200, json.dumps({"message" : "Finished"}), content_type='application/json')
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
        if self.request.method == 'POST':
            body = json.loads(self.request.body)
            user = User(**body)
            shifts = mongodbDataAdapter.loadShifts(user)
            self.response.send(200, json.dumps(shifts), content_type='application/json')
        else:
            self.response.send(400, 'Bad Request')

class LoginPage(Route):

    def handle(self):
        # serve the index.html file
        with open('./views/login.html', 'r') as f:
            self.response.send(200, f.read(), content_type='text/html')


class MainPage(Route):
    
    def handle(self):
        with open('./views/main.html', 'r') as f:
            self.response.send(200, f.read(), content_type='text/html')
        pass

class StaticFile(Route):
    def handle(self):
        with open(f'.{self.request.uri}', 'r') as f:
            self.response.send(200, f.read(), content_type='text/css')
    pass

class DownloadShift(Route):
    def handle(self):
        if self.request.method == 'GET':
            print(self.request.uri)
            shift_id = self.request.uri.split('/')[-1]
            shift = mongodbDataAdapter.loadShift(shift_id)
            shift_df = shift.getShift()
            filename = f'{shift_id}.csv'
            shift_df.to_csv(filename, index=False)
            with open(filename, 'r') as f:
                content = f.read()
            self.response.send(200, content, content_type='text/csv')
        else:
            self.response.send(400, 'Bad Request')


class AddRegistry(Route):

    def handle(self):
        if self.request.method == 'POST':
            body = json.loads(self.request.body)
            body['status'] = "ON"
            registry = Registry(**body)
            mongodbDataAdapter.addRegistry(registry)
            self.response.send(200, 'Finish')
        else:
            self.response.send(400, 'Bad Request')

class DeleteRegistry(Route):

    def handle(self):
        if self.request.method == 'POST':
            body = json.loads(self.request.body)
            body['status'] = "OFF"
            registry = Registry(**body)
            mongodbDataAdapter.addRegistry(registry)
            self.response.send(200, 'Finish')
        else:
            self.response.send(400, 'Bad Request')      

class MicroserviceHealthCheckRoute(Route):

    def handle(self):
        if self.request.method == 'GET':
            self.response.send(200, json.dumps({'status' : 'healthy'}), content_type='application/json')

class GetHealthCheck(Route):

    def handle(self):
        if self.request.method == 'GET':
            registry = mongodbDataAdapter.getHealthCheck()

            health_services = []
            for i in range(len(registry)):
                if registry[i]['status'] == "ON":
                    response = requests.get(registry[i]['healthcheck'])
                    data = response.json()
                    if data['status'] == 'healthy':
                        health_services.append(registry[i]) 
            self.response.send(200, json.dumps(health_services), content_type='application/json')
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
                self.response.send(json.dumps({"message": "status", "status": "received"}))
            problem = json.loads(received_message)
            solver = self.solver_type(problem)
            self.response.send(json.dumps({"message": "status", "status": "compiling"}))
            solver.compile()
            self.response.send(json.dumps({"message": "status", "status": "solving"}))
            shifts = solver.solve()
            self.response.send(json.dumps({"message": "status", "status": "finished"}))
            self.response.send(json.dumps({"message": "result", "result": shifts}))




if __name__ == '__main__':
    server = ProtocolTypeRouter({
        'http': HttpServer(routes=[
            (r'/$', LoginPage),
            (r'/shift$', MainPage),
            (r'/login$', Login),
            (r'/static/(.*)$', StaticFile),
            (r'/user', GetUser), (r'/updateusershifts', UpdateUserShifts), 
            (r'/saveshift', SaveShift), (r'/loadshift$', LoadShift), 
            (r'/loadshifts$', LoadShifts),
            (r'/download/', DownloadShift),
            (r'/registry/add', AddRegistry), (r'/registry/delete', DeleteRegistry),
            (r'/gethealthcheck', GetHealthCheck)
        ]),
    })
    server.run()