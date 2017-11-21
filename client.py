#!/usr/bin/python
import socket
from os import system

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

    def run(self):
        while True:
            data = self.recieve()                          
            print data
            resp = raw_input(">> ")
            self.send(resp)
            system("clear")

c = Client(port=2222)                
c.run()

