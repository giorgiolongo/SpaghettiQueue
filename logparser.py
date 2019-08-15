from PyQt5.QtCore import pyqtSignal, QThread
from threading import Timer
from time import sleep
from datetime import datetime
from spaghettiqueue.client import InvalidUUID, GenericAPIError
from traceback import format_exc

class LogsParser(QThread):
    def __init__(self, client, latestfilepath, substring, parent = None):
        super(LogsParser, self).__init__(parent)
        self.path = latestfilepath
        self.client = client
        self.substring = substring
        
        #Counter that checks if the position doesnt change for 5 minutes, in that case it considers the position as frozen
        self.freezetimer = Timer(300, self.on_freeze)
        
        #Current status of the Thread
        self.status = "running"
        
    #Pyqtsignals declatation. The way to comunicate between the ui and the QThread
    update_sign = pyqtSignal(str, str) #position update
    status_sign = pyqtSignal(str) #change of status between online/offline/frozen
    error_sign = pyqtSignal(str) #shows a popup if error encountered in LogsParser thread
    invaliduuid_sign = pyqtSignal()

    def on_freeze(self):
        """
        What happens if the position doesnt change for 5 minutes
        """
        self.client.freeze()
        self.status = "frozen"
        self.status_sign.emit("frozen")
        self.freezetimer.cancel()
        self.freezetimer = Timer(300, self.on_freeze)
        self.freezetimer.start()

    def stop(self):
        """
        Prevents timer thread from running after closing the gui
        """
        self.freezetimer.cancel()
        self.freezetimer = Timer(300, self.on_freeze)
        self.status = "stopped"


    def run(self):
        lastPosition = -1 #Position cache
        self.freezetimer.start()
        while True:
            if self.status != "stopped":
                try:
                    lines = open(self.path, 'r').read().splitlines() #Opens the latest.log file, splits it in a list, and reads the last line
                    if self.substring in lines[-1]: #Checks if the queue substring is contained in the line
                        currentPosition = lines[-1].split(" ")[-1] #Parses last part of the line(the actual value)
                        if currentPosition != lastPosition: #If the position is changed, it updates the server and the GUI. Also it resets the freezetimer
                            self.freezetimer.cancel()
                            self.freezetimer = Timer(300, self.on_freeze)
                            self.freezetimer.start()

                            if self.status != "running":
                                self.status = "running"
                                self.status_sign.emit("running")
                            self.update_sign.emit(currentPosition, datetime.now().strftime("%X"))
                            self.client.update(currentPosition)
                            lastPosition = currentPosition
                    

                except InvalidUUID: #If the uuid becomes invalid it generates a new one
                    self.invaliduuid_sign.emit()
                    sleep(3)
                    continue
                except GenericAPIError as e: #Generic error happened
                    self.error_sign.emit(e)
                    sleep(5)
                    continue

                except IndexError:
                    pass
                except:
                    self.error_sign.emit(format_exc())
                    sleep(5)
                    continue
            sleep(20)