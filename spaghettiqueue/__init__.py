from configparser import ConfigParser
from spaghettiqueue.logparser import LogsParser
from spaghettiqueue.client import APIClient
from spaghettiqueue.ui import Spaghetti
from PyQt5.QtWidgets import QApplication
from sys import platform, exit
from os import getenv
from os.path import expanduser, join, isfile

def main():
    #Initializing configuration file parser anc checking if config file exists. if not it creates one with default values
    config = ConfigParser()

    if isfile('spaghetti.ini'):
        config.read('spaghetti.ini')
    else:
        config['spaghettiqueue'] = {
            'mcpath': join(getenv('APPDATA') if platform == "win32" else expanduser('~'), ".minecraft"),
            'hostip': 'https://api.spaghettiqueue.app',
            'uuid': "", 
            "queuesubstring": "Position in queue:" 
            }
        config.write(open('spaghetti.ini', 'w'))

    # Init Classes. the client which comunicates between the app and the api server, the parser which parses the data from the latest.log file and the ui
    latestfilepath = join(config['spaghettiqueue']['mcpath'], "logs", "latest.log") #path of the latest.log file in .minecraft/logs
    queuesubstring = config['spaghettiqueue']['queuesubstring']

    client = APIClient(uuid=config['spaghettiqueue']['uuid'], host=config['spaghettiqueue']['hostip'])

    config['spaghettiqueue']['uuid'] = client.uuid
    config.write(open('spaghetti.ini', 'w'))

    app = QApplication([""])
    parser = LogsParser(client, latestfilepath, queuesubstring)
    ui = Spaghetti(client, parser, config)
    ui.setupUi()
    ui.show()
    exit(app.exec_())


if __name__ == "__main__":
    main()