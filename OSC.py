from src.server.server import ProtocolTypeRouter, HttpServer, WebSocketServer
from src.server.route import Route, WebSocketRoute

import json
from src.algorithms.Solvers import SASolver

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

class SAWebsocketRoute(SolverWebsocketRoute):

    def __init__(self, request, response):
        super().__init__(request, response, SASolver)


if __name__ == '__main__':
    server = ProtocolTypeRouter({
        'websocket': WebSocketServer(routes=[
                (r'/sa', SAWebsocketRoute)
            ])
        })
    server.run()
