#!/usr/bin/python
import socket
from os import system
from time import sleep
import sys 
import threading

class Client(object):
    def __init__(self, host='localhost', port=2222):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error, msg:
            print("Failed to create Socket. Error: "+str(msg[0]))
        self.host = host
        self.port = port
        self.s.connect((self.host,self.port)) 
        self.data = None
    
    #def recieve(self):
    #    return self.s.recv(4096)
    def recieve(self):
        self.data = self.s.recv(4096)
        print self.data

    def send(self,data):
        self.s.send(data)

    def testGame(self, username, password):
        # 1 login, username, pass, 2 gameslist, 1 firstgame, 1easy
        print("len argv: ", len(sys.argv))
        if len(sys.argv) > 2:
            username = sys.argv[1]
            password = sys.argv[2]
            print username
            print password
        
        selectionSequence = ["1", username, password,"2", "1", "1"]
        for s in selectionSequence:
            data = self.recieve()                          
            print data
            self.send(s)
            sleep(0.5)
        return 
        
         
    def run(self):
        #self.testGame("Robert","mypass")
        while True:
            data = self.recieve()                          
            print data
            resp = raw_input(">> ")
            while resp == "":
                print("[!] Invalid input!\n")
                print self.data
                resp = raw_input(">> ")
            
            self.send(resp)
            print("\n\n")
            #system("clear")

# NOTE: the client must be threaded
# The raw_input function is a blocking function that is
# stopping the client from recieving the updated
# game state. 

c = Client(port=1222)                
c.run()




