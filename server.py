import socket
from thread import *
import sys

class Server(object):
    def __init__(self, host='', port=2222):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error, msg:
            print("Socket creation failed")
        self.host = host
        self.port = port 
        try:
            self.s.bind((self.host,self.port))
        except socket.error, msg:
            print("Bind Failed")
            
        self.numConnections = 10
        self.players = []
        self.s.listen(self.numConnections)
        self.conn = None
        self.data = None
        self.hallOfFameList = ["Tom", "Dick","Harry"]
        self.usersList = [] 
        self.gamesList = ["Game1","Game2"]
        self._populateData()
        self.request = {"hall":self.hall, 
                        "login":self.login,
                        "makeUser":self.makeUser,
                        "games":self.games,
                        "difficulty":self.difficulty}

    def _populateData(self):
        f = open("users.txt",'r')
        for user in f.readlines():
            user,paswd = user.strip().split(" ") 
            self.usersList.append((user,paswd))
        f.close()
   
    def makePkt(self, cmd, data):
        cmd = str(cmd.strip())
        if isinstance(data,list):
            data = str(" ".join([word.replace(" ", "_") for word in data]))
        else:
            data = str(data.strip())
        return cmd +" "+ data

    def unPackPkt(self,data):
        #command is first argument, data is the rest
        d = data.strip().split(" ")
        return d[0], d[1:]

    ######### Menu Option Responses ############
    def login(self):
        print("Processing Login")
        for user, paswd in self.usersList:
            if user == self.data[0] and paswd == self.data[1]:
                print("User: ", user, " Authenticated!")
                return self.makePkt("game","True")
        print("[!]Authentication Failed!")
        return self.makePkt("menu","False")

    def hall(self):
        print("Retrieving Hall of Fame...")
        menu_cmd = self.data[0]
        return self.makePkt(menu_cmd,self.hallOfFameList) 
    
    def makeUser(self):
        print("Making User...")
        f = open('users.txt', 'a')
        creds = self.data[0] + " " + self.data[1] + "\n"
        f.write(creds)
        f.close()
        return self.makePkt("menu","True")
   
    def games(self):
        print("Retrieving Games List...")
        if self.data[0] == "False" and self.data[1] == "True" and self.data[2] == "False":
            return self.makePkt("game",self.gamesList)
        
        if self.data[0] == "True" and self.data[1] == "False" and self.data[2] == "False":
            return self.makePkt("difficulty","True")

    def difficulty(self):
        self.difficultyLevel = int(self.data[0])
        print("Set difficulty to: ", self.difficultyLevel)
        return self.makePkt("playgame",str(self.difficultyLevel))
    ######### END Menu Option Responses ############

    def process(self,conn, players):
        while True:
            d = conn.recv(1024)
            if d == "":
                break

            #print("Recieved: ", self.unPackPkt(d))
            (cmd, self.data) = self.unPackPkt(d)
            if cmd in self.request:
                conn.send(self.request[cmd]())
            else:
                print("[!] recieved Invalid packet")
                #sys.exit()
                    
    def run(self):
        while True:
            # wait to accept connection (blocking call)
            conn, addr = self.s.accept()
            if addr not in self.players:
                self.players.append((conn,addr))
            self.process(conn,self.players)


if __name__ == "__main__":
    s = Server(port=2221)
    s.run()
