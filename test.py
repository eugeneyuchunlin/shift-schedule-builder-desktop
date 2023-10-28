from PySide6.QtWebSockets import QWebSocket
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QUrl

from src.model.data_adapter import RemoteDataAdapter
import json

if __name__ == '__main__':

    #-------getUser----------
    #user = RemoteDataAdapter().getUser("guest123", "guest123")
    #print(user.toJson())

    #-------updateusershifts-------
    #getuser = RemoteDataAdapter().getUser("guest123", "guest123")
    #print(getuser.toJson())
    #print("=====================================")
    #updateuser = RemoteDataAdapter().updateUserShifts(getuser)
    #print(updateuser)


    #-------saveshift--------
    getuser = RemoteDataAdapter().getUser("guest123", "guest123")
    getshift = RemoteDataAdapter().loadShift("10a67b34-dede-4a99-97ef-8f0b76927947")
    print(getuser.toJson())
    print(getshift.toJson())
    print("=========================================")
    saveshift = RemoteDataAdapter().saveShift(getuser, getshift)
    print(saveshift)

    #-------loadShift--------
    #shift = RemoteDataAdapter().loadShift("10a67b34-dede-4a99-97ef-8f0b76927947")
    #print(shift.toJson())
    

    #-------loadShifts--------
    #getuser = RemoteDataAdapter().getUser("guest123", "guest123")
    #shifts = RemoteDataAdapter().loadShifts(getuser)
    #print(shifts)