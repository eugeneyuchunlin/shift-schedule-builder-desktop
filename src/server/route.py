import socket
import json
import struct

class Response(object):

    def __init__(self, client_socket:socket.socket):
        self._client_socket = client_socket
        pass
    
    def close(self):
        self._client_socket.close() 

    def socket(self):
        return self._client_socket

class HttpResponse(Response):
    def __init__(self, client_socket:socket.socket):
        self._client_socket = client_socket
        pass

    def send(self, code, message, content_type="text/html"):
        
        response = f"HTTP/1.1 {code}\r\n"
        response += f"Content-Type: {content_type}\r\n"
        response += "Connection: close\r\n"
        response += f"Content-Length: {len(message)}\r\n"
        response += "\r\n"
        response += message + "\r\n"

        self._client_socket.send(response.encode('utf-8'))
        self._client_socket.close()


class WebSocketResponse(Response):

    def send(self, message):
        response_data = struct.pack('B', 0x81) + struct.pack('B', len(message)) + message.encode('utf-8')
        self._client_socket.send(response_data)

class Request(object):

    def __init__(self, client_socket: socket.socket):
        self._client_socket = client_socket

        # get the HTTP request
        request = self._client_socket.recv(2048).decode('utf-8')
        request_lines = request.split('\r\n')  # Split the request into lines

        # Parse the request line to get method, URI, and protocol
        request_line_parts = request_lines[0].split(' ')
        self.method = request_line_parts[0]
        self.uri = request_line_parts[1]
        self.protocol = request_line_parts[2]
        self.request = request

        self.headers = {}
        self.body = ""
        # Parse headers and body
        for line in request_lines[1:]:
            if line:
                header_name, header_value = line.split(': ', 1)
                self.headers[header_name] = header_value
            else:
                # An empty line marks the end of headers and the start of the body
                self.body = '\r\n'.join(request_lines[request_lines.index('') + 1:])
                # read remaining bytes
                if 'Content-Length' in self.headers:
                    content_length = int(self.headers['Content-Length'])
                    remaining_bytes = content_length - len(self.body)
                    self.body += self._client_socket.recv(remaining_bytes).decode('utf-8')
                break
    def socket(self):
        return self._client_socket



class Route(object):

    def __init__(self, request: Request, response: Response):
        self.request = request
        self.response = response
        pass
    
    def handle(self):
        pass


class WebSocketRoute(Route):

    def __init__(self, request: Request, response: WebSocketResponse):

        self.request = request
        self.response = response
        self._client_socket = request.socket()

    def _decode_websocket_data(self, data):
        opcode = data[0] & 0x0F
        payload_length = data[1] & 0x7F
        mask_key = data[2:6]
        encoded_data = data[6:]

        decoded_data = bytearray(len(encoded_data))
        for i in range(len(encoded_data)):
            decoded_data[i] = encoded_data[i] ^ mask_key[i % 4]

        return opcode, decoded_data

    def _recv(self, size=2048):
        try:
            data = self._client_socket.recv(size)
            print(data)
            if len(data) == 0:
                self.close()
                return None

            opcode, decoded_data = self._decode_websocket_data(data)

            if opcode == 1:
                message = decoded_data.decode('utf-8')
                return message
            elif opcode == 8:
                response_data = struct.pack('B', 0x88) + struct.pack('B', 0)
                self._client_socket.send(response_data)
                self.close()
                return None
        except ConnectionResetError:
            self.close()
        

    def close(self):
        self._client_socket.close()

class TestRoute(Route):

    def handle(self):
        print(self.request.method)
        print(self.request.uri)
        print(self.request.protocol)
        print(self.request.headers)
        print(self.request.body)
        data = {
            "message": "successful"
        }
        self.response.send(200, json.dumps(data), content_type="application/json")


class EchoWebsocketRoute(WebSocketRoute):

    def handle(self):
        while True:
            received_message = self._recv()
            print("Received Text: ", received_message)
            if received_message is None:
                break
            else:
                self.response.send("Good!")