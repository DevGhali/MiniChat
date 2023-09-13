import select
import socket
import time
from _thread import *

# GLOBAL VARIABLES
connected_users = []
clients = []
banner = """
  __  __ _       _    _____ _           _   
 |  \/  (_)     (_)  / ____| |         | |  
 | \  / |_ _ __  _  | |    | |__   __ _| |_ 
 | |\/| | | '_ \| | | |    | '_ \ / _` | __|
 | |  | | | | | | | | |____| | | | (_| | |_ 
 |_|  |_|_|_| |_|_|  \_____|_| |_|\__,_|\__|
 server-side                     by DevGhali
"""
instructions = """\n\n
*** Run the client's script with 2 arguments -> \
1. IP where the server is broadcasting 
2. PORT where its listening\n
---EXAMPLE---
xyz@xyz:~/xyz$ python client.py 172.0.0.1 8080\n\n
*** Afterwards pick a nickname and provide a valid username and password\n
---EXAMPLE---
Enter Username : JohnB
Enter Password : 1234n\n\n
"""


def validate(name, input_user, input_pass):
    if input_user in valid_users and valid_users[input_user] == input_pass:
        msg = "Access Granted! User : {}".format(name)
        print(msg)
        return 1
    else:
        msg = "User {} tried logging in with wrong credentials".format(name)
        print(msg)
        return 0


# Broadcasts a message sent by a user to all other users connected
def broadcast(message, conn):
    for client in clients:
        if client != conn:
            try:
                client.send(message)
            except:
                client.close()
                remove(client)


def remove(conn):
    if conn in clients:
        clients.remove(conn)


# initializes a thread for each new client
def thread(conn, name, username):
    msg = "Welcome {} to this chatroom!".format(name)
    conn.send(msg)

    while True:
        try:
            message = conn.recv(2048)
            if message and conn.connect:
                _message = "<{}> {}".format(name, message)
                print(_message)
                broadcast(_message, conn)
            else:
                remove(conn)
                connected_users.remove(username)
        except:
            continue


# initializes the server
def server_startup():
    print("Starting Server....")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((IP, PORT))
    server.listen(100)
    sockets = [server]
    print("Server is up connect some clients!")
    return server, sockets


# a checkpoint to identify the user and authorise the login
def checkpoint(conn):
    while 1:
        conn.send("Enter name :")
        name = conn.recv(2048).strip()
        conn.send("Enter Username : ")
        username = conn.recv(2048).strip()
        if username in connected_users:
            conn.send("User already connected! \ntry again\n")
            continue
        conn.send("Enter Password : ")
        password = conn.recv(2048).strip()
        if not validate(name, username, password):
            msg = "Wrong Credentials! try again \n\n"
            conn.send(msg)
            continue
        else:
            connected_users.append(username)
            conn.send("1")
            return name, username


# Dictionary with usernames snd passwords  "username":"password"
valid_users = {
    '1': '2',
    '2': '3',
    '3': '4'
}

IP = "127.0.0.1"
PORT = 8080


def main():
    server, sockets = server_startup()
    while True:
        read_sockets, _, exception_sockets = select.select(sockets, [], sockets)
        for x in read_sockets:
            if x == server:
                conn, addr = server.accept()
                clients.append(conn)
                sockets.append(conn)
                name, username = checkpoint(conn)
                start_new_thread(thread, (conn, name, username))


if __name__ == "__main__":
    print(banner)
    time.sleep(2)
    print(instructions)
    time.sleep(2)
    main()
