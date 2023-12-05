from src.server.server import ProtocolTypeRouter, HttpServer, WebSocketServer
from src.server.route import Route, WebSocketRoute

import json
from src.algorithms.Solvers import DAUSolver
from server import SolverWebsocketRoute

class DAUWebsocketRoute(SolverWebsocketRoute):

    def __init__(self, request, response):
        super().__init__(request, response, DAUSolver)

if __name__ == '__main__':
    server = ProtocolTypeRouter({
        'websocket': WebSocketServer(routes=[
                (r'/dau', DAUWebsocketRoute)
            ])
        }, port=8889)
    server.run()