from src.server.server import ProtocolTypeRouter, HttpServer, WebSocketServer
from src.server.route import Route, WebSocketRoute
import requests
import json
from src.algorithms.Solvers import DAUSolver
from server import SolverWebsocketRoute, MicroserviceHealthCheckRoute

class DAUWebsocketRoute(SolverWebsocketRoute):

    def __init__(self, request, response):
        super().__init__(request, response, DAUSolver)


def deleteRegistry():
    print("Shutting down server")
    requests.post("http://localhost:8888/registry/delete", json={"service": "DAU"})

if __name__ == '__main__':
    server = ProtocolTypeRouter({
        'http' : HttpServer(routes=[
                (r'/healthcheck', MicroserviceHealthCheckRoute)
        ]),
        'websocket': WebSocketServer(routes=[
                (r'/dau', DAUWebsocketRoute)
            ])
        }, port=8889, terminate_function=deleteRegistry)

    requests.post("http://localhost:8888/registry/add", json={
        
        "healthcheck": "http://localhost:8889/healthcheck",
        "service": "DAU", 'url' : "ws://localhost:8889/dau"
    }) 
    server.run()
    print("Server shut down")