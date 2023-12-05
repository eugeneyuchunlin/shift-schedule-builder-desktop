from src.server.server import ProtocolTypeRouter, HttpServer, WebSocketServer
from src.server.route import Route, WebSocketRoute

import json
import requests
from src.algorithms.Solvers import SASolver
from server import SolverWebsocketRoute

class SAWebsocketRoute(SolverWebsocketRoute):

    def __init__(self, request, response):
        super().__init__(request, response, SASolver)

def deleteRegistry():
    print("Shutting down server")
    requests.post("http://localhost:8888/registry/delete", json={"service": "SA"})

if __name__ == '__main__':
    server = ProtocolTypeRouter({
        'websocket': WebSocketServer(routes=[
                (r'/sa', SAWebsocketRoute)
            ])
        }, port=8890, terminate_function=deleteRegistry)
    
    requests.post("http://localhost:8888/registry/add", json={"service": "SA"}) 
    server.run()
