from requests import post, get

class APIClient:
    def __init__(self, uuid: str = "", host: str="https://api.spaghettiqueue.app/"):
        self.requrl = host + "/requuid.php" #requests a uuid to the server - self.requuid()
        self.updateurl = host + "/qupdate.php" #updates the position referred to that uuid in the database - self.update()
        self.delurl = host + "/deluuid.php" #removes the uuid from the database and requests a new one - self.changeuuid()
        self.freezeurl = host + "/qfreeze.php" #sets the status to frozen - self.freeze()
        self.versionurl = "https://api.spaghettiqueue.app/version.php" #gets the version of the api running on the MAIN server - self.checkupdates()
        self.version = "alpha1" #api version - self.checkupdates()
        
        #if no uuid passed to the class it generates a new one
        if uuid == "":
            self.uuid = self.getuuid()
        else:
            self.uuid = uuid
    
    def getuuid(self):
        """
        Sends a GET request to the php api asks for a compleatly new uuid. 
        The answer will be the new uuid, if not the answer will be Error: <error message> and an exception will be rised by the _errorhandler
        """
        req = get(self.requrl)
        if "Error: " in req.text:
            self._errorhandler(req.text)
        else:
            self.uuid = req.text
            return req.text
    def update(self, position: str):
        """
        Sends a POST request to the php api containing the uuid and the updated position. 
        The answer can be OK if everything went right, if not the answer will be Error: <error message> and an exception will be rised by the _errorhandler
        """
        req = post(self.updateurl, data={"position": position, "uuid": self.uuid})
        if req.text != "OK":
            self._errorhandler(req.text)
    
    def freeze(self):
        """
        Sends a POST request to the php api requiring to set the stauts to frozen. 
        The answer can be OK if everything went right, if not the answer will be Error: <error message> and an exception will be rised by the _errorhandler
        """
        req = post(self.freezeurl, data={"uuid": self.uuid})
        if req.text != "OK":
            self._errorhandler(req.text)
    
    def changeuuid(self):
        """
        Sends a POST request to the php api containing the old uuid asking for a new uuid one. 
        The server will compleatly remove the old one and replace it with the new generated one.
        The answer will be the new uuid, if not the answer will be Error: <error message> and an exception will be rised by the _errorhandler
        """
        req = post(self.delurl, data={"uuid": self.uuid})
        if "Error: " in req.text:
            self._errorhandler(req.text)
        else:
            self.uuid = req.text
            return req.text

    def checkupdates(self):
        """
        Checks if the Version of the client matches the one on the server and return True if they dont, which means that an update is available
        """
        return not get(self.versionurl).text == self.version



    def _errorhandler(self, errormsg: str):
        """
        Parses server given errors and turns them into Python exceptions
        """
        if "Invalid uuid" in errormsg:
            raise InvalidUUID
        elif "Missing" in errormsg:
            raise NoArgument
        else:
            raise GenericAPIError(errormsg)



#Exception Classes

class InvalidUUID(Exception):
    pass

class NoArgument(Exception):
    pass

class GenericAPIError(Exception):
    pass