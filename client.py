#!/usr/bin/python
import socket
from os import system
<<<<<<< HEAD
from time import sleep
import sys 
import threading
=======
import sys
from time import sleep
>>>>>>> temp

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

<<<<<<< HEAD
=======
    # checks if response is required
    def isResponse(self,data):
        if len(data.split("#")) <2:
            return False
        return True

    def killSignal(self,sig):
        if sig == "q!":
            return True
        return False

>>>>>>> temp
    def testGame(self, username, password):
        # 1 login, username, pass, 2 gameslist, 1 firstgame, 1easy
        print("len argv: ", len(sys.argv))
        if len(sys.argv) > 2:
            username = sys.argv[1]
            password = sys.argv[2]
<<<<<<< HEAD
=======
            print "Logining in the user: "
>>>>>>> temp
            print username
            print password
        
        selectionSequence = ["1", username, password,"2", "1", "1"]
        for s in selectionSequence:
            data = self.recieve()                          
            print data
            self.send(s)
            sleep(0.5)
        return 
<<<<<<< HEAD
        
         
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
=======

    def run(self):
        #self.testGame("Robert", "mypass")
        while True:
            data = self.recieve()                          
            #print("Data: ", data)
            if self.killSignal(data):
                break
            # is Response Required
            if self.isResponse(data):
                data = data.split('#')[1]
                print data
                resp = raw_input(">> ")
                while resp == "":
                    print("[!] Invalid input!\n")
                    print data
                    resp = raw_input(">> ")
                self.send(resp)
            else:
                #print "no hashtag"
                print data
        print("Exiting server")
        self.s.close()
        sys.exit()
>>>>>>> temp

c = Client(port=2222)                
c.run()




