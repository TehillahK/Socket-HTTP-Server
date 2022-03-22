import socket
import threading
import sys
import os
import uuid
import json
import tempfile
from ssl import VERIFY_X509_TRUSTED_FIRST
class Server:
    def __init__(self,port) :
        self._port = port
        self._host = ''
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self._host,self._port))
        self.html =  '''
        HTTP/1.1 200 OK
        Content-Length: {}
        '''
    
    def threading_function(self,conn,addr):
        print(f"Connected by ${addr}")
        data = conn.recv(1024)
        if data:
            print(data)
        conn.close()

    def start(self):
        print("Starting server")
        self.socket.listen()
        while True:
            conn,addr = self.socket.accept()
            conn.settimeout(20)
            print("Server has started")
            new_thread = threading.Thread(target=self.threading_function,args=(conn,addr))
            new_thread.start()
           # conn.close() # Close connection
            

def main():
    myServer = Server(port = int(sys.argv[1]))
    myServer.start()

if __name__ == "__main__":
    print()
    main()