import socket
from thread import *
import sys
from menu import ClientMenu
from users import Player
from game import Hangman

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
        self.hallOfFameList = ["Tom", "Dick","Harry"]
        self.usersList = [] 
        self.gamesList = ["Game1","Game2"]
        self.state = 0
        self._populateData()

    def _populateData(self):
        f = open("users.txt",'r')
        for user in f.readlines():
            user,paswd = user.strip().split(" ") 
            self.usersList.append((user,paswd))
        f.close()

    def process(self,conn, players):
        while True:
            menu = ClientMenu(conn=conn, usersFilename="users.txt",
                              gameList=self.gamesList, 
                              hallOfFameList=self.hallOfFameList)
        
            connection, username, difficulty = menu.run() 
            #Pass these parameters into Game or Player object
            player = Player(name=username, conn=connection)
            print("players name: ", player.name)
            hangman = Hangman()
            hangman.difficulty = difficulty
            hangman.join(player)
            hangman.play()

    def run(self):
        while True:
            # wait to accept connection (blocking call)
            conn, addr = self.s.accept()
            if addr not in self.players:
                self.players.append((conn,addr))
            self.process(conn,self.players)


if __name__ == "__main__":
    s = Server(port=1222)
    s.run()
