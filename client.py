import socket
from menu import ClientMenu

class Client(object):
    def __init__(self, host='localhost', port=2222):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error, msg:
            print("Failed to create Socket. Error: "+str(msg[0]))
        self.host = host
        self.port = port
        self.s.connect((self.host,self.port)) 
        self.menu = ClientMenu()
        self.request = None
    
    def recieve(self):
        d = self.s.recv(4096)
        return self.unpack(d) 

    def isValidCreds(self):
        pass

    def makePkt(self,data):
        return " ".join(data)

    def unpack(self,data):
        d = data.strip().split(" ")
        return d[0], d[1:]

    def send(self,data):
        #print("Sending: ", data)
        self.s.send(data)

    def run(self):
        cmd = "menu"
        data = None
        while True:
            if cmd == "menu":
                d= self.menu.mainMenu()
                self.send( self.makePkt(d))            

            elif cmd == "game":
                d = self.menu.games()
                self.send( self.makePkt(d))

            elif cmd == "difficulty":
                d = self.menu.difficultyMenu()
                self.send(self.makePkt(d))

            elif cmd == "playgame":
                print("In Play game mode.. lets play hangman")

            cmd, data = self.recieve()                          
            print("Recieved: ", data)

c = Client(port=2221)                
c.run()
