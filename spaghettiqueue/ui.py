from PyQt5.QtWidgets import QMainWindow, QMessageBox, QLabel, QFrame, QPushButton, QApplication
from PyQt5.QtCore import QSize, QRect, Qt
from PyQt5.QtGui import QIcon
import spaghettiqueue.icons as icons
from spaghettiqueue.qr import genqrpixmap
from subprocess import Popen
from traceback import format_exc
from spaghettiqueue.client import InvalidUUID
from sys import platform
from ctypes import windll
from webbrowser import open as browseropen



class Spaghetti(QMainWindow):
    def __init__(self, client, parser, config, parent=None):
        QMainWindow.__init__(self, parent) 
        self.client = client
        self.parser = parser
        self.config = config
        self._want_to_close = False

    def setupUi(self):
        """
        Checks for updates and opens a popup if one is available
        """
        if self.client.checkupdates(): #check for updates dialog
            updatebox = QMessageBox.question(self,"A new update is available!", "A new update is available, do you want to download it?", QMessageBox.Yes | QMessageBox.No)
            if updatebox == QMessageBox.Yes:
                browseropen("https://spaghettiqueue.app/update?v=" + self.client.version)

        """
        Setups the ui
        """
        self.setObjectName("SpaghettiQueue")
        self.setWindowTitle("SpaghettiQueue")
        self.setWindowIcon(icons.b64toicon(icons.spaghettiraw))
        if platform == "win32": 
            windll.shell32.SetCurrentProcessExplicitAppUserModelID(u' ') #To make the icon appaer in the taskbar

        self.x = 325
        self.y = 145
        self.resize(self.x, self.y)
        self.setMinimumSize(QSize(self.x, self.y))
        self.setMaximumSize(QSize(self.x, self.y))

        self.text1 = QLabel(self)
        self.text1.setGeometry(QRect(10, 10, 91, 16))
        self.text1.setObjectName("text1")
        self.text1.setText("Position:")

        self.text2 = QLabel(self)
        self.text2.setGeometry(QRect(10, 30, 110, 14))
        self.text2.setObjectName("text2")
        self.text2.setText("Last position change:")

        self.text3 = QLabel(self)
        self.text3.setGeometry(QRect(10, 70, 96, 14))
        self.text3.setObjectName("text3")
        self.text3.setText("Status:")

        self.text4 = QLabel(self)
        self.text4.setGeometry(QRect(10, 50, 55, 14))
        self.text4.setObjectName("text4")
        self.text4.setText("Your uuid:")

        self.qrview = QLabel(self)
        self.qrview.setGeometry(QRect(190, 12, 125, 125))
        self.qrview.setObjectName("qrview")
        self.qrview.setFrameShape(QFrame.Box)
        self.qrview.setFrameShadow(QFrame.Plain)
        self.qrview.setLineWidth(1)
        self.qrview.setAlignment(Qt.AlignCenter)
        self.qrview.setPixmap(genqrpixmap(self.client.uuid)) #generates the qrcode
        
        self.statusbtn = QPushButton(self)
        self.statusbtn.setGeometry(QRect(10, 107, 65, 30))
        self.statusbtn.setObjectName("statusbtn")
        self.statusbtn.setText("Stop")
        
        self.reloadbtn = QPushButton(self)
        self.reloadbtn.setGeometry(QRect(80, 107, 65, 30))
        self.reloadbtn.setObjectName("reloadbtn")
        self.reloadbtn.setText("New uuid")
        
        self.settingsbtn = QPushButton(self)
        self.settingsbtn.setGeometry(QRect(150, 107, 30, 30))
        self.settingsbtn.setObjectName("settingsbtn")
        self.settingsbtn.setIcon(icons.b64toicon(icons.settingsraw))
        self.settingsbtn.setIconSize(QSize(20,20))
        
        self.queuevalue = QLabel(self)
        self.queuevalue.setGeometry(QRect(52, 11, 110, 14))
        self.queuevalue.setObjectName("queuevalue")
        self.queuevalue.setText("Waiting for updates...")
        
        self.lastupdate = QLabel(self)
        self.lastupdate.setGeometry(QRect(114, 30, 47, 14))
        self.lastupdate.setObjectName("lastupdate")
        
        self.statuslabel = QLabel(self)
        self.statuslabel.setGeometry(QRect(48, 70, 47, 14))
        self.statuslabel.setObjectName("statuslabel")
        self.statuslabel.setText("Running")
        self.statuslabel.setStyleSheet('color: lime')
        
        self.uuidlabel = QLabel(self)
        self.uuidlabel.setGeometry(QRect(62, 50, 120, 14))
        self.uuidlabel.setObjectName("uuidlabel")
        self.uuidlabel.setText(self.client.uuid)
        self.uuidlabel.setToolTip("You can copy your uuid from here")
        self.uuidlabel.setTextInteractionFlags(Qt.TextSelectableByMouse)
        
        "Button clicks and thread signals connect to functions"
        self.settingsbtn.clicked.connect(self._opensettings)
        self.reloadbtn.clicked.connect(self._newuuid)
        self.statusbtn.clicked.connect(self._switchstatus)


        "Signal connects and Thread start"
        self.parser.update_sign.connect(self._update)
        self.parser.invaliduuid_sign.connect(self._invaliduuid)
        self.parser.error_sign.connect(self._errordialog)
        self.parser.status_sign.connect(self._updatestatus)
        self.parser.start()
    


    "Buttons connect functions"

    def _opensettings(self):
        """
        It opens the config file with the default system text editor
        If something fails an error dialog comes up
        """
        try:
            Popen("start /WAIT spaghetti.ini", shell=True)
        except:
            self.errordialog(format_exc())

    def _newuuid(self):
        """
        Asks to the API for a new uuid and replaces the one in the label, the qr as well as the one in the config file
        If something fails an error dialog comes up
        """
        try:
            self.client.changeuuid()
        except InvalidUUID:
            self.client.getuuid()
        except:
            self._errordialog(format_exc())
        self.uuidlabel.setText(self.client.uuid)
        self.qrview.setPixmap(genqrpixmap(self.client.uuid))
        self.config['spaghettiqueue']['uuid'] = self.client.uuid
        self.config.write(open('spaghetti.ini', 'w'))

    def _switchstatus(self):
        """
        Changes the state based on the status button press
        """
        if self.parser.status == "stopped":
            self.statuslabel.setText("Running")
            self.statuslabel.setStyleSheet('color: Lime')
            self.statusbtn.setText("Stop")
            self.parser.status = "running"
        else:
            self.parser.stop()
            self.statusbtn.setText("Start")
            self.statuslabel.setText("Stopped")
            self.statuslabel.setStyleSheet('color: Red')
    

    "Signal connect fucntions"
    def _invaliduuid(self):
        self._newuuid()
        self._errordialog('The uuid was invalid. New one was created')
    
    def _updatestatus(self, status):
        """
        Changes status from frozen to running and vice-versa
        """
        if status == "frozen":
            self.statuslabel.setText("Frozen")
            self.statuslabel.setStyleSheet('color: Aqua')
        else:
            self.statuslabel.setText("Running")
            self.statuslabel.setStyleSheet('color: Lime')

    def _update(self, position, datestamp):
        self.queuevalue.setText(position)
        self.lastupdate.setText(datestamp)

    def _errordialog(self, error):
        """
        Error dialog
        """
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Critical)
        msgBox.setText("Error: " + error + "\nWaiting 5 seconds...")
        msgBox.setWindowTitle("An error occurred")
        msgBox.exec()

    "Prevent from closing without quitting from threads"
    def closeEvent(self, event):
        self.parser.stop()

            
