from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from select import select
import sys
import json
from threading import Thread
from os import execlp, fork
addr = "linux8.csie.org"
port = 1487

server = socket(AF_INET, SOCK_STREAM)
server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server.bind((addr, port))
server.listen(1024)

fdset = [server]
user_sock = {}
sock_addr = {}
sock_user = {}

def read_from_server(conn_sock):
    try:
        msg = conn_sock.recv(1024)
        if not len(msg):
            return False
        return msg.decode()
    except Exception as e:
        print("The exception appears to be")
        print(e)
        return False

while True:
    readset, outset, errset = select(fdset, [], [], 0)
    for isset in readset:
        if isset == server:
            conn_fd = server.accept()
            conn_sock, conn_addr = conn_fd
            print(f"Got a new connection from {conn_addr[0]}")
            fdset.append(conn_sock)
            sock_addr[conn_sock] = conn_addr[0]
            conn_sock.send("Enter your username".encode("utf-8"))
        else:
            if isset not in sock_user:
                username = read_from_server(isset)
                if not username:
                    print(f"\033[91m{isset} disconnected\033[0m")
                    fdset.remove(isset)
                    isset.close()
                    continue
                print(f"\033[94mWe have a new user {username}\033[0m")
                user_sock[username] = isset
                sock_user[isset] = username

                setting = { "type" : "setting", "body" : {} , "set" : 1}
                for user in user_sock:
                    setting["body"][user] = sock_addr[user_sock[user]]
                setstr = json.dumps(setting)
                for i in fdset:
                    if i != server:
                        i.send(setstr.encode("utf-8"))
            else:
                msg = read_from_server(isset)
                user = sock_user[isset]
                addr = sock_addr[isset]
                if not msg:
                    print(f"\033[91m{user} from {addr} disconnected\033[0m")
                    setting = { "type": "setting", "user" : user, "addr" : addr, "set": 0}
                    setstr = json.dumps(setting)
                    for i in fdset:
                        if i != server:
                            i.send(setstr.encode("utf-8"))
                    del user_sock[user]
                    del sock_user[isset]
                    fdset.remove(isset)
                    isset.close()
                else:
                    try:
                        j = json.loads(msg)
                        body_type = j["type"]
                        to = j["to"]
                        body = j["body"]
                        if body_type == "string":
                            del j["to"]
                            j["from"] = user
                            user_sock[to].send((json.dumps(j)).encode("utf-8"))
                        elif body_type == "file":
                            del j["to"]
                            j["from"] = user
                            user_sock[to].send((json.dumps(j)).encode("utf-8"))
                            
                        print(f"from {sock_user[isset]}", j, type(j))
                    except Exception as e:
                        isset.send("\033[91mInvalid Format!\033[0m".encode("utf-8"))
                        print("\033[91merror:\033[0m", "from", sock_user[isset], type(sock_user[isset]), msg, type(msg))
                        continue
            #msg = json.loads(msg)
            #print(msg)
