from src.server.server import ProtocolTypeRouter, HttpServer, WebSocketServer
from src.server.route import Route

from src.model.data_adapter import DataAdapter
import json

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


if __name__ == '__main__':
    server = ProtocolTypeRouter({
        'http': HttpServer(routes=[
            (r'/user', GetUser)
        ]),
        # 'websocket': WebSocketServer(routes=[(r'/chat', EchoWebsocketRoute)])
    })
    server.run()