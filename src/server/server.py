import socket
import hashlib
import base64
import struct
import threading
import re
import signal
import sys

from .route import TestRoute, Request, Response, EchoWebsocketRoute, WebSocketResponse, HttpResponse


class ProtocolTypeRouter(object):

    def __init__(self, protocols, bind='localhost', port=8888):
        self.HOST = bind
        self.PORT = port

        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self._server_socket.bind((bind, port))
        self._server_socket.listen(5)

        self._protocols = protocols

        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)


    def handle(self, client_socket):
        pass

    def shutdown(self, signum, frame):
        self._server_socket.close()
        sys.exit(0)

    def routing(self, client_socket):
        # if protocol is http
        try:
            request = Request(client_socket)
            if 'Upgrade' in request.headers and request.headers['Upgrade'] == 'websocket':
                response = WebSocketResponse(client_socket)            
                self._protocols['websocket'].handle(request, response)
            else:
                response = HttpResponse(client_socket)
                self._protocols['http'].handle(request, response) 
        except Exception as e:
            response = HttpResponse(client_socket)
            response.send(500, 'Internal Server Error')
            raise(e)

        pass

    def run(self):
        if 'http' in self._protocols:
            print(f"Server is running on http://{self.HOST}:{self.PORT}")

        if 'websocket' in self._protocols:
            print(f"Websocket server is running on ws://{self.HOST}:{self.PORT}")

        try:
            while True:
                client_socket, addr = self._server_socket.accept()
                client_handler = threading.Thread(target=self.routing, args=(client_socket,))
                client_handler.start()
        except KeyboardInterrupt:
            self._server_socket.close()


class Server(object):

    def __init__(self, routes=[]):
        self._routes = routes
        pass

    def handle(self):
        pass


class HttpServer(Server):
    
    def __init__(self, routes=[]):
        super().__init__(routes)
        pass


    def handle(self, request:Request, response:Response):
        # get uri of the request
        print(f"[{request.method}]: {request.uri}")
        uri = request.uri
        for i in range(len(self._routes)):
            reg = re.compile(self._routes[i][0])
            if reg.match(uri):
                route = self._routes[i][1](request, response)
                route.handle()
                break

class WebSocketServer(Server):

    def __init__(self, routes=[]):
        super().__init__(routes)
        pass

    def _create_handshake_response(self, request:Request):
        key =  request.headers['Sec-WebSocket-Key'].encode('utf-8')
        guid = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
        response_key = base64.b64encode(hashlib.sha1(key + guid.encode('utf-8')).digest()).decode('utf-8')
    
        response = "HTTP/1.1 101 Switching Protocols\r\n"
        response += "Upgrade: websocket\r\n"
        response += "Connection: Upgrade\r\n"
        response += f"Sec-WebSocket-Accept: {response_key}\r\n\r\n"
    
        return response
    
    def decode_websocket_data(self, data):
        opcode = data[0] & 0x0F
        payload_length = data[1] & 0x7F
        mask_key = data[2:6]
        encoded_data = data[6:]

        decoded_data = bytearray(len(encoded_data))
        for i in range(len(encoded_data)):
            decoded_data[i] = encoded_data[i] ^ mask_key[i % 4]

        return opcode, decoded_data

    def handle(self, request:Request, response:Response):
                # routing to websocket route handler

        # get uri of the request
        match = False
        uri = request.uri
        for i in range(len(self._routes)):
            reg = re.compile(self._routes[i][0])
            if reg.match(uri):
                match = True
                handshake_response = self._create_handshake_response(request)
                response.socket().send(handshake_response.encode('utf-8'))

                route = self._routes[i][1](request, response)
                route.handle()
                break
        if match == False:
            response.close()







# Handle WebSocket connections


# Create a socket server
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.bind((HOST, PORT))
# server_socket.listen(5)
# 
# print(f"WebSocket server is listening on ws://{HOST}:{PORT}")
# 
# while True:
#     client_socket, addr = server_socket.accept()
#     client_handler = threading.Thread(target=handle_websocket, args=(client_socket,))
#     client_handler.start()


if __name__ == '__main__':
    server = ProtocolTypeRouter({
        'http': HttpServer(routes=[(r'/', TestRoute)]),
        'websocket': WebSocketServer(routes=[(r'/chat', EchoWebsocketRoute)])
    })
    server.run()
    pass