all: server client

server:
	gcc fileserver.c -o server
client: 
	gcc fileclient.c -o client
