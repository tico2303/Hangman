#!/usr/bin/python
import socket
from os import system
import sys
from time import sleep

class Client(object):
    def __init__(self, host='localhost', port=2222):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error, msg:
            print("Failed to create Socket. Error: "+str(msg[0]))
        self.host = host
        self.port = port
        self.s.connect((self.host,self.port)) 
    
    def recieve(self):
        return self.s.recv(4096)

    def send(self,data):
        self.s.send(data)

    # checks if response is required
    def isResponse(self,data):
        if len(data.split("#")) <2:
            return False
        return True

    def killSignal(self,sig):
        if sig == "q!":
            return True
        return False

    def testGame(self, username, password):
        # 1 login, username, pass, 2 gameslist, 1 firstgame, 1easy
        print("len argv: ", len(sys.argv))
        if len(sys.argv) > 2:
            username = sys.argv[1]
            password = sys.argv[2]
            print "Logining in the user: "
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

c = Client(port=2222)                
c.run()

