from src.server.server import ProtocolTypeRouter, HttpServer, WebSocketServer
from src.server.route import Route, WebSocketRoute
import requests
import json
from src.algorithms.Solvers import DAUSolver
from server import SolverWebsocketRoute

class DAUWebsocketRoute(SolverWebsocketRoute):

    def __init__(self, request, response):
        super().__init__(request, response, DAUSolver)

def deleteRegistry():
    print("Shutting down server")
    requests.post("http://localhost:8888/registry/delete", json={"service": "DAU"})

if __name__ == '__main__':
    server = ProtocolTypeRouter({
        'websocket': WebSocketServer(routes=[
                (r'/dau', DAUWebsocketRoute)
            ])
        }, port=8889)

    requests.post("http://localhost:8888/registry/add", json={"service": "DAU", 'url' : "ws://localhost:8889/dau"}) 
    server.run()
    print("Server shut down")