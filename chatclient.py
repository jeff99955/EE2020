import socket 
import select 
import sys 
import argparse
import json
from os import fork, wait, execlp

BUFFER_SIZE = 2048

user_addr = {}
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
                    if not message:
                        print("\033[AConnection Broken")
                        exit(1)
                    try:
                        data = json.loads(message)
                        if data["type"] == "string":
                            print("from {}: {}".format(data["from"], data["body"]))
                        elif data["type"] == "file":
                            print("received", data)
                            pid = fork()
                            if pid == 0:
                                execlp("./server", "./server")
                            status = wait()
                            print("server returned", status[0])
                        elif data["type"] == "setting":
                            i = data["set"]
                            if i:
                                config = data["body"]
                                for u in config:
                                    user_addr[u] = config[u]
                                print("user_addr=>", user_addr)
                            else:
                                user = data["user"]
                                del user_addr[user]
                    except ValueError:
                        print("valueError")
                        print(message.decode())
                    except KeyError as e:
                        print("keyError", e)
                        pass
                else:
                    message = sys.stdin.readline().strip("\n")
                    print(message)
                    try:
                        data = json.loads(message)
                        if data["type"] == "string":
                            client.send(message.strip("\n").encode())
                        elif data["type"] == "file":
                            client.send(message.strip("\n").encode())
                            to_ip = user_addr[data["to"]]
                            filename = data["body"]
                            pid = fork()
                            if pid == 0:
                                print(to_ip, filename)
                                execlp("./client", "./client", to_ip, filename)
                            status = wait()
                            if status[1]:
                                print("Cannot send the file")
                            else:
                                print("Succeed in sending files")   
                    except ValueError:
                        client.send(message.encode("utf-8"))
                    
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
