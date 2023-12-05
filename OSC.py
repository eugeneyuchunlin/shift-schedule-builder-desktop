from src.server.server import ProtocolTypeRouter, HttpServer, WebSocketServer
from src.server.route import Route, WebSocketRoute

import json
from src.algorithms.Solvers import SASolver
from server import SolverWebsocketRoute

class SAWebsocketRoute(SolverWebsocketRoute):

    def __init__(self, request, response):
        super().__init__(request, response, SASolver)


if __name__ == '__main__':
    server = ProtocolTypeRouter({
        'websocket': WebSocketServer(routes=[
                (r'/sa', SAWebsocketRoute)
            ])
        }, port=8890)
    server.run()
