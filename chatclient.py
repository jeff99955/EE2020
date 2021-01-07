import socket 
import select 
import sys 
import argparse
import json

BUFFER_SIZE = 2048

def main(args):

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    ip = "linux8.csie.org"
    port = 1487
    client.connect((ip, port))
    while True: 
        try:
            sockets_list = [sys.stdin, client] 
            read_sockets, write_socket, error_socket = select.select(sockets_list,[],[]) 
          
            for socks in read_sockets:
                if socks == client:
                    message = socks.recv(BUFFER_SIZE)
                    print(message.decode())
                else:
                    message = sys.stdin.readline().strip("\n")
                    try:
                        data = json.loads(message)
                        if data["type"] == "string":
                            client.send(message.strip("\n").encode())
                        elif data["type"] == "file":
                            with open(data["body"], "rb") as f:
                                client.sendfile(f, 0)
                            client.send(b'done')
                    except ValueError:
                        client.send(message.encode("utf-8"))
            if not message:
                print("\033[AConnection Broken")
                break
        except KeyboardInterrupt:
            break
    client.close() 

if __name__ == "__main__":
    prog = "client.py"
    descr = "client side of chat room"
    parser = argparse.ArgumentParser(prog=prog, description=descr)
    parser.add_argument("--ip", type=str, required=False)
    parser.add_argument("--port", type=int, required=False)
    arguments = parser.parse_args()
    main(arguments)
