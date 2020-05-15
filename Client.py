import socket
import pickle
import sys


# Class is used to connect to the Server
class Network:
    host = sys.argv[1]
    pot = sys.argv[2]

    def __init__(self):
        # Initializes socket.
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = socket.gethostbyname(self.host)
        self.port = int(self.pot)
        self.addr = (self.server, self.port)
        self.pos = self.connect()

    def getPos(self):
            return self.pos

    def connect(self):
        try:
            # Connects client to the server
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(1024))
        except socket.error as e:
            print("Server Connection Error: " + str(e))
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            print("Positions: ", data)
            return pickle.loads(self.client.recv(1024))
        except socket.error as e:
            print(e)



