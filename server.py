#   server.py
#   Tehillah Kangamba 7859367   
#   Comp3010
#   Assignment 2
#   http server library
import socket
import threading
import sys
import os
import uuid
import json
import tempfile
from cookies import Cookies, SessionCookie
from httpParser import file_type, get_body, has_cookie, is_api_req, serve_static_file
from header import http_header

class Server:
    def __init__(self,port) :
        self._port = port
        self._host = ''
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self._host,self._port))
        self._api = None
        #self.socket.settimeout(30)

    #gets file name and returns file content
    def add_api(self,api):
        print("api added")
        self._api = api
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
        is_api_req(route)
        if file_exists and filetype == "html":
            body = self.get_resource(file_path)
            data_length = len(body)
            myhtml = http_header( code=200 ,message="OK",size = data_length)
            print(body)
            res = myhtml + "\n" + body
            print(res)
            result = res.encode()
        elif file_exists and filetype == "jpeg":
            body = self.get_img_resource(file_path)
            data_length = len(body)
            myhtml = http_header( code=200 ,message="OK",size = data_length,type = "image/jpeg")
            header = f"{myhtml}\n"
            res = header.encode()+ body
           #  print(res)
            result = res
        elif file_exists == False:
            #failed
            print("file not found")
            body = self.get_resource("static/NotFound.html")
            data_length = len(body)
            myhtml = http_header(code=404,message="Not Found",size = data_length)
            print(body)
            res = myhtml + "\n" + body
            print(res)
            result = res.encode()
        return result
    
    def handle_api_req(self,type,req,body = None):
        result = b''
        print("handling api request")
        if body != None:
            self._api.set_body(body)
        result = self._api.listen(type,req)
        return result
    
    def threading_function(self,conn):
        data = conn.recv(1024)
        res = None
        html_body = None
        if data:
            req = data.decode()
            
            #   Check if req has a cookie
            if has_cookie(req) == False:
                cookie = SessionCookie()
                res = cookie.get_cookie().encode()
                print(res)
                conn.sendall(res)

            req_arr = req.split()
            req_type = req_arr[0]
            req_route = req_arr[1]
            if req_type=="POST" or req_type=="PUT":
                html_body = get_body(req)
            if is_api_req(req_route) and has_cookie(req):
                res = self.handle_api_req(req_type,req_route,body=html_body)
            elif is_api_req(req_route) and (has_cookie(req)==False):   # user has no cookie
                body = "user not authorized"
                data_length = len(body)
                myhtml = http_header(code=403,message="Not Found",size = data_length)
                print(body)
                res = myhtml + "\n" + body
                print(res)
                res = res.encode()
            else:
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
            
            

