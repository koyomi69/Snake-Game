import socket
from _thread import *
import pickle
import random
import sys

host = sys.argv[1]
pot = sys.argv[2]
num = sys.argv[3]

server = socket.gethostbyname(host)
port = int(pot)

width = 600
height = 400

# AF_INET = ipv4 & SOCK_STREAM = TCP
# Initializes socket.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Binds socket.
try:
    print("Binding server and port")
    s.bind((server, port))
except socket.error as e:
    print("Bind error: " + str(e) + "\n")
# Opens up the port and now can start connecting to clients
# Listening only once to see if there is anything on that server port
# A blank will mean unlimited connections
s.listen(2)
print("Waiting for a Connection, Server Started")
pos = [(random.randrange(1, (width - 20), 10), random.randrange(1, (height - 20), 10)),
       (random.randrange(1, (width - 30), 10), random.randrange(1, (height - 30), 10))]

numberofPlayers = int(num)
connections = []


# Threading allows for functions to run simultaneously
def snake_positions(conn, player):
    conn.sendall(pickle.dumps(pos[player]))
    reply = ""
    # Continuously run while our client is still connected
    while True:
        try:
            # Larger this size is, longer it takes time to receive information
            # 1024 = packet size
            data = pickle.loads(conn.recv(1024))
            pos[player] = data
            if not data:
                print("Disconnected")
                conn.close()
                break
            else:
                print("Received : ", data)
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]
                print("Sending: ", reply)
            conn.sendall(pickle.dumps(reply))
        except:
            # exit()
            break

    print("Lost Connection")
    conn.close()


def waiting_for_connections():
    global conn, addr
    playersAvailable = 0
    while len(connections) < numberofPlayers:
        try:
            conn, addr = s.accept()
            connections.append(conn)
        except socket.error as err:
            print("Connection Error: " + str(err) + "\n")
        print("Connected to : ", addr)
        start_new_thread(snake_positions, (conn, playersAvailable))
        playersAvailable += 1

        
waiting_for_connections()
while True:
    continue
