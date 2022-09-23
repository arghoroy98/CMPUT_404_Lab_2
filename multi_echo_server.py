#!/usr/bin/env python3

#Note: All code is from Lab_2 Monday Video (https://drive.google.com/file/d/1TD8UR9o-GPaudPNsY9HrePzroRBsEBFe/view?usp=sharing)

import socket
import time
from multiprocessing import Process

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        #QUESTION 3
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        s.bind((HOST, PORT))
        #set to listening mode
        s.listen(2)
        
        #continuously listen for connections
        while True:
            conn, addr = s.accept()
            print("Connected by", addr)
            p = Process(target=handle_multi_echo, args=(addr, conn))
            p.daemon = True
            p.start()
            print("Started process ", p)

def handle_multi_echo(addr, conn):
    print("Connected by", addr)
    full_data = conn.recv(BUFFER_SIZE)
    conn.sendall(full_data)
    conn.close()

if __name__ == "__main__":
    main()
