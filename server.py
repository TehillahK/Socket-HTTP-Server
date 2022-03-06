import socket , sys , threading
class Server:
    def __init__(self,port) :
        self._port = port
        self.socket =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.bind(self._port)

    def start(self):
        print("Starting server")
        self.socket.listen()
        while True:
            print("Server has started")
            

def main():
    myServer = Server(port = 80)
    myServer.start()

if __name__ == "__main__":
    
    print(sys.argv[1])
    main()