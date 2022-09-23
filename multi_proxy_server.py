# Code from Lines 4 to 44 is from Lab_2 Monday Video (https://drive.google.com/file/d/1TD8UR9o-GPaudPNsY9HrePzroRBsEBFe/view?usp=sharing)
# Code from Lines 45 to 62 is taken from examples in Lab_2 Monday Video (https://drive.google.com/file/d/1TD8UR9o-GPaudPNsY9HrePzroRBsEBFe/view?usp=sharing)

import socket
import sys
import time
from multiprocessing import Process

HOST  = ""
PORT = 8001
BUFFER_SIZE = 1024

def get_remote_ip(host):
    print('Getting IP for ' + HOST)
    try:
        remote_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print('Could not resolve hostname. Exiting')
        sys.exit()

    print(f'Ip address of {host} is {remote_ip}')
    return remote_ip

def main():
    host = 'www.google.com'
    port = 80 
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
        print('Starting proxy server')
        #allow reused addresses, bind, and set to listening node
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_start.bind((HOST, PORT))
        proxy_start.listen(1)

        while True:
            conn, addr = proxy_start.accept()
            print("Connected by", addr)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                print("Connecting to Google")
                remote_ip = get_remote_ip(host)

                #connect proxy_end
                proxy_end.connect((remote_ip, port))
                p = Process(target=handle_multiple_clients, args=(addr, conn, proxy_end))
                p.daemon = True
                p.start()
                print("Started process ", p)

def handle_multiple_clients(addr, conn, proxy_end):
    #send data
    send_full_data = conn.recv(BUFFER_SIZE)
    print(f"Sending received data {send_full_data} to google")
    proxy_end.sendall(send_full_data)
                
    #SHUTTING DOWN
    proxy_end.shutdown(socket.SHUT_WR)

    data = proxy_end.recv(BUFFER_SIZE)
    print(f"Sending received data {data} to client")
    conn.send(data)
    conn.close()

if __name__ == "__main__":
    main()