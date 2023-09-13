import select
import socket
import time
import sys
from _thread import *

banner = """
  __  __ _       _    _____ _           _   
 |  \/  (_)     (_)  / ____| |         | |  
 | \  / |_ _ __  _  | |    | |__   __ _| |_ 
 | |\/| | | '_ \| | | |    | '_ \ / _` | __|
 | |  | | | | | | | | |____| | | | (_| | |_ 
 |_|  |_|_|_| |_|_|  \_____|_| |_|\__,_|\__|
 client-side                     by DevGhali
"""


def setup_connection(argv):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((str(argv[1]), int(argv[2])))
    return server


def main():
    if len(sys.argv) != 3:
        print("Usage: python client.py SERVER_IP SERVER_PORT\n")
        exit()
    server = setup_connection(sys.argv)
    flag = 0
    while True:
        sockets = [sys.stdin, server]
        try:
            read_sockets, _, error_socket = select.select(sockets, [], [])
        except select.error:
            server.shutdown(2)
            server.close()
            print('error connecting')
            break
        for socks in read_sockets:
            if socks == server:
                message = socks.recv(2048).strip()
                if message == "1":
                    flag = 1
                    continue
                else:
                    print(message)
            else:
                message = sys.stdin.readline()
                server.send(message)
                if flag:
                    sys.stdout.write("<you>")
                    sys.stdout.write(message)
                    sys.stdout.flush()


if __name__ == "__main__":
    print(banner)
    time.sleep(2)
    main()
