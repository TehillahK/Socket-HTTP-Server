import socket
import threading
import sys
import os
import uuid
import json
import tempfile
from cookies import Cookies
from httpParser import file_type, serve_static_file

class Server:
    def __init__(self,port) :
        self._port = port
        self._host = ''
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self._host,self._port))
        self.success_http ='''
HTTP/1.1 200 OK
Content-Length: {}
'''     
        self.success_img_http ='''
HTTP/1.1 200 OK
Content-Length: {}
Content-Type: image/jpeg
'''
        self.body = '''<html>
<body>
<h1>You are a winner</h1>
You are the {}nth comsomter
</body>
</html>
'''
    #gets file name and returns file content
    def get_resource(self,resource):
        result = ""
        with open(resource) as f:
            result = f.read()
        return result

    def get_img_resource(self,resource):
        result = ""
        with open(resource,"rb") as f:
            result = f.read()
        return result

    def handle_req(self,typeReq,route):
        result = b""
        print(f"{typeReq},{route}")
        filename , file_path ,filetype = serve_static_file(route)
        file_exists = os.path.exists(file_path)
        print(filename)
        print(f"file exists {file_exists}")
        print(f"file type {filetype}")

        if file_exists and filetype == "html":
            body = self.get_resource(file_path)
            data_length = len(body)
            myhtml = self.success_http.format(data_length)
            print(body)
            res = myhtml + "\n" + body
            print(res)
            result = res.encode()
        elif file_exists and filetype == "jpeg":
            body = self.get_img_resource(file_path)
            data_length = len(body)
            myhtml = self.success_http.format(data_length)
            header = f"{myhtml}\n"
            res = header.encode()+ body
           #  print(res)
            result = res
        else:
            #failed
            print("file not found")
        # if typeReq =="GET" and route == "/":
        #     body = self.get_resource("static/index.html")
        #     data_length = len(body)
        #     myhtml = self.success_http.format(data_length)
        #     print(body)
        #     res = myhtml + "\n" + body
        #     print(res)
        #     result = res.encode()
        # elif typeReq =="GET" and route == "/images.html":
        #     body = self.get_resource("static/images.html")
        #     data_length = len(body)
        #     myhtml = self.success_http.format(data_length)
        #     res = myhtml + "\n" + body
        #     result = res.encode()
        # elif typeReq =="GET" and route == "/test.html":
        #     body = self.get_resource("static/test.html")
        #     data_length = len(body)
        #     myhtml = self.success_http.format(data_length)
        #     print(body)
        #     res = myhtml + "\n" + body
        #     print(res)
        #     result = res.encode()
        # elif typeReq =="GET" and route == "/images/binary.jpeg":
        #     body = self.get_img_resource("static/images/binary.jpeg")
        #     data_length = len(body)
        #     myhtml = self.success_http.format(data_length)
        #     header = f"{myhtml}\n"
        #     res = header.encode()+ body
        #   #  print(res)
        #     result = res
        # else:
        #     failed_http = '''
        #     HTTP/1.1 200 OK
        #     Content-Length: {}
        #     '''
        #     failed_body = '''<html>
        #     <body>
        #     Not found
        #     </body>
        #     </html>
        #     '''
        #     data_length = len(failed_body)
        #     myhtml = failed_http.format(data_length)
        #     res = myhtml + "\n" + failed_body
        #     result = res.encode()
        #     print(result)
        return result
    
    def threading_function(self,conn):
      #  print(f"Connected by ${addr}")
        data = conn.recv(1024)
        if data:
            #print(req)
            req = data.decode()
            print(req)
            req = req.split()
            req_type = req[0]
            req_route = req[1]
            res = self.handle_req(req_type,req_route)
            conn.sendall(res)
        
        conn.close()

    def start(self):
        print("Starting server")
        self.socket.listen()
        while True:
            print("Server has started")
            conn,addr = self.socket.accept()
            print(f"connected ${addr}")
            new_thread = threading.Thread(target=self.threading_function,args=(conn,))
            new_thread.start()
           # conn.close() # Close connection
            
            

def main():
    myServer = Server(port = int(sys.argv[1]))
    myServer.start()

if __name__ == "__main__":
    print()
    main()