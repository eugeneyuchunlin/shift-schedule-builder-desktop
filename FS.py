from src.server.server import ProtocolTypeRouter, HttpServer, WebSocketServer
from src.server.route import Route, WebSocketRoute
import requests
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

    try:
        requests.post("http://localhost:8000/registry/add", json={"service": "DAU"}) 
        server.run()
    except KeyboardInterrupt:
        requests.post("http://localhost:8000/registry/delete", json={"service": "DAU"}) 
        print("Shutting down server")
        print("Server shut down")