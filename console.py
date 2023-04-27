from PySide6.QtCore import Signal, QObject

class Logger(QObject):

    log_signal = Signal(str)

    def __init__(self):
        super().__init__()
        pass

    def log(self, *args):
        print(args)
        msg = ' '.join([str(arg) for arg in args])
        self.log_signal.emit(str(msg))