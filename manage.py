import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from subprocess import Popen

class Handler(FileSystemEventHandler):

    def reload(self, event):
        if event.is_directory:
            return
        elif event.event_type == 'modified':
            os.system('pkill -f "python3 server.py"')
            print("Restarting server...")
            time.sleep(1)
            Popen(['python3', 'server.py'])


    def on_any_event(self, event):
        self.reload(event)



if __name__ == '__main__':
    event_handler = Handler()
    Popen(['python3', 'server.py'])
    src_observer = Observer()
    src_observer.schedule(event_handler, path='./src/server', recursive=True)
    src_observer.start()

    server_observer = Observer()
    server_observer.schedule(event_handler, path='./server.py', recursive=True)
    server_observer.start()
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        server_observer.stop()
        src_observer.stop()

    server_observer.join()
    src_observer.join()