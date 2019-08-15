## Disclamer
After some tests within the discord server I discovered that http polling on an app which updates that fast is the worst thing I could do. I was about to implement a socket system but without having any experience in socket design It's taking a lot of time which I dont have at the moment. I released the app with a poll rate of 30s so the app is not instat but it's the only way to make the system usable without flooding the server. I also had to upgrade the server and to maintain it alive I added a small adbar at the bottom of the android app, sorry about that but it's necessary. The socket system will be available later on as well as the webapp for iOS users. I raccomand to update when the update popup comes up.

# SpaghettiQueue Destkop App
Check your 2b2t position in queue via Android Phone/Webapp.

The source code of the Android app is not out yet. It will be released in days, just to publish a refactored version of it. Meanwhile you can download the APK as well as the Windows Client [from the Release page.](https://github.com/giorgioshine/SpaghettiQueue/releases/tag/alpha)

The API Source Code and documentation can be found at [Here](http://github.com/giorgioshine/SpaghettiQueueAPI) 

Make sure to join our discord server

[![Join Discord Server](https://img.shields.io/badge/Join%20our-Discord-%237289da)](https://discord.gg/tAWtPUW) ![License](https://img.shields.io/github/license/giorgioshine/SpaghettiQueue) 
### Desktop app installation
There is a pre-compiled all in one EXE or you can run the program directly from the source with python3.
You can download the EXE from the release page if you trust me enought.

#### Requirements
```
PyQt5==5.12.2
qrcode==6.1
```
#### Installation
After cloning the source code and extracting it, install the program by running:
```
pip3 install -r requirements.txt
python3 setup.py install
```


#### Running
```
python -m spaghettiqueue
```

### Contributing
Please feel free to contribute to the development of the project by improving the existing code or creating your own app based on the SpaghettiAPI. If you do I raccomand joining the discord server


### License
[MIT License](http://github.com/giorgioshine/SpaghettiQueue/LICENSE)


### Todos
* [ ] Android Notifications 
* [ ] Web client
* [ ] SpaghettiQueue.app website
* [X] Destkop Client
* [ ] API docs
* [ ] WebSocket-based client and server


### Donations
If you found the project useful, you can give me a cup of coffee :) 

[![Donate](https://img.shields.io/badge/Donate-PayPal-blue.svg)](http://paypal.me/spaghettiqueue)
