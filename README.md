# EE2020

## Server Side
The server side is independent from the environment which we need to setup later in the client side. One should change 
```
addr = "linux8.csie.org"
```
to their real ip address or on their remote server address so that the server could be connected (as it will be reniced on this server and might be terminated by the admin if using CPU for prolonged time). After setting up, run the program by
```
python3 server.py
```
---
## Client Side
To test this project, one should set up the environment first at the client side(supporting Python 3.5~3.8). After activating the virtual environment, run ```make``` to install the dependencies and compile the file sending application.
After ```make```,
1. change 
```
ip = "linux8.csie.org"
```
to the aforementioned address
2. change
```
path_to_python3 = "/usr/bin/python3"
```
to the path to python
3. run the application
```
python3 client.py
```


## Some defect
The files won't send sometimes since using the address provided by Python may not be static address