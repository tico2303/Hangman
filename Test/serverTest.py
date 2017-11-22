import socket
import sys
from thread import *
from menuTest import GameTest, Users

HOST = '' # means available on all interfaces
PORT = 8333 # arbitrary port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
print "Socket Create"

try:
    s.bind((HOST,PORT))
except socket.error, msg:
    print "Bind failed, Error: " +str(msg[0]) + " Message: " + msg[1]
    sys.exit()

print "Socket bind complete"

num_connections = 10
s.listen(num_connections)

#function handling connections. This will be used to create threads
def clientthread(conn,clients):
    #Sending message to connnected client
    user.conn.send("Welcome to server. Type something and hit enter\n") #send takes string
    #loop so fucntion doesnt terminate and thread does no end
    while True:
        #Receiving from client
        data = user.conn.recv(1024)
        reply = "OK..." + data
        print "addr: ", addr
        data = data.strip().split(" ")
        cmd = data[0]
        msg = " ".join(data[1:])+"\n"
        

        if not data:
            break
        if cmd == "!q":
            break

        game = GameTest()
        game.addPlayer(user)
        game.run()
        curr_conn = conn
        if cmd == "!sendall":
            print "[!sendall] Sending to all"
            for cn,address in clients:
                if cn != conn:
                    cn.sendto(msg,(address[0], address[1]))
                    curr_conn = cn 
        conn.sendall(reply)
    
    conn.close()
    clients.remove(curr_conn)

# create list of clients
clients = []
while 1:

    #wait to accept a connection -blocking call
    conn, addr = s.accept()
    user = User()
    user.conn = conn
    user.addr = addr
    if addr not in clients:
        clients.append(user)
    #display client info
    print "connection with " + addr[0] + ":" + str(addr[1])

    #start new thread takes 1st arg as a function name to be run, 2nd is the tuple of arguments to the function.
    start_new_thread(clientthread,(user,clients)

s.close()

