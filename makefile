all: server client
	pip3 install numpy opencv-python==4.4.0.46 Pillow==8.0.1 PyQt5==5.15.1 tensorflow opencv-python==4.4.0.46 PyQt5==5.15.1
server:
	gcc fileserver.c -o server
client: 
	gcc fileclient.c -o client
