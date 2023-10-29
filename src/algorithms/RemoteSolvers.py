from PySide6.QtWebSockets import QWebSocket
from PySide6.QtCore import QUrl, QEventLoop, Signal
from PySide6.QtWidgets import QApplication
import json



class RemoteSolver(QWebSocket):
    
    finished = Signal(list)
    status = Signal(str)
    def __init__(self, url):
        super().__init__()
        # establish connection
        self.url = url
        self.connected.connect(self.on_connected)
        self.textMessageReceived.connect(self.on_message)
        self.disconnected.connect(self.on_closed)

    def socket_connect(self, url=None):
        print("Connecting to " + self.url)
        if url is None and self.url is None:
            raise Exception("No url provided")
        elif url is not None:
            self.url = url
            self.open(QUrl(url))
        else:
            self.open(QUrl(self.url))
        
        # Create an event loop to wait for the connection to be established
        self.event_loop = QEventLoop()
        self.event_loop.exec()

    def on_connected(self):
        self.event_loop.quit()

    def solve(self, problem):
        print("Sending problem...")
        problem_body = json.dumps(problem)
        self.sendTextMessage(problem_body)

    def on_message(self, message):
        data = json.loads(message)
        print(data)
        if "result" in data:
            self.finished.emit(data["result"]) 

        elif "status" in data:
            self.status.emit(data["status"])       


    def on_closed(self):
        pass


class RemoteDAUSolver(RemoteSolver):
    
    def __init__(self):
        super().__init__(url="ws://localhost:8888/dau")


class RemoteSASolver(RemoteSolver):

    def __init__(self):
        super().__init__(url="ws://localhost:8888/sa")


if __name__ == '__main__':
    app = QApplication([])
    remote_solver = RemoteSolver("ws://localhost:8888/sa")
    remote_solver.socket_connect()
    remote_solver.solve({"message" : "good"})
    app.exec()