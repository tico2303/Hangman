#!/usr/bin/python
import socket
import threading
from thread import start_new_thread
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
        self.s.listen(self.numConnections)
        
    def run(self):
        raise NotImplementedError

    def close(self):
        self.s.close()

menuLock =threading.Lock() 
gameLock =threading.Lock()
playersListLock = threading.Lock()

class HangmanServer(Server):
    def __init__(self, host='', port=2222):
        super(HangmanServer,self).__init__(host,port)
        #self.usersList = []
        self.players = []
        self.hallOfFameList = ["Tom", "Dick","Harry"]
        self.gamesList = [Hangman(name="HangmanA"), Hangman(name="HangmanB")]
        self.gameDict = {}
        #self._populateData()

    """
    def _populateData(self):
        f = open("users.txt",'r')
        for user in f.readlines():
            user,paswd = user.strip().split(" ") 
            self.usersList.append((user,paswd))
        f.close()

    def broadcast(self,connection,message):
        for player in self.players:
            if player.conn != connection:
                try:
                    player.conn.send(message)
                except: 
                    # socket is broken
                    player.conn.close()
                    #remove from players list
        
    """
    def updateGameDict(self, gameName, player):
        if gameName not in self.gameDict.keys():
            self.gameDict[gameName] = {}
            self.gameDict[gameName]["playersList"] = []
            self.gameDict[gameName]["playersList"].append(player)
        else:
            if player not in self.gameDict[gameName]["playersList"]:
                self.gameDict[gameName]["playersList"].append(player)

    def process(self,player, playersList):
        #whle True
        while player in playersList:
            menu = ClientMenu(player=player, usersFilename="users.txt",
                              gameList=self.gamesList, 
                              hallOfFameList=self.hallOfFameList)
        
            player, gameChoice, difficulty = menu.run() 
            #player.send("Done With Menu\n")
            #print("players name: ", player.name)
            #print("players addr: ", player.addr)
            #print("[!] Failed in Menu processing")

            print("[+] gameChoice: ", gameChoice)

            #create new game
            if gameChoice not in self.gamesList:
                print("[+] Creating New Game")
                #print "gameChoice in gamesList: ", gameChoice.name 
                hangman = Hangman(name=player.name)
                #self.updateGameDict(hangman, player) 
                #print "gameDict: ", self.gameDict
                self.gamesList.append(hangman)
                print("[+] Playing: ", hangman.name)
                hangman.difficulty = difficulty
                hangman.add(player)
                active = hangman.play()

            #join existing game
            else:
                #print("gameChoice: ", gameChoice.getName(), " NOT in gamesList")
                print("[+] Joining ", gameChoice)
                hangman = None
                for game in self.gameList:
                #for game in self.gameDict.keys():
                    if game.name == gameChoice.name:
                        game.add(player)
                        hangman = game
                print("Playing: ", hangman.name)
                if not hangman.active:
                    hangman.play()
                
                
                
    def run(self):
        print("[+] Hangman Server\n")
        while True:
            # wait to accept connection (blocking call)
            conn, addr = self.s.accept()
            player = Player(conn=conn,addr=addr)
            if player not in self.players:
                self.players.append(player)
           
            try: 
                #self.process(player,self.players)
                t = threading.Thread(target=self.process,args=(player,self.players))
                t.daemon = True
                t.start()
            except:
                print("[!] Failed to create Thread")


if __name__ == "__main__":
    s = HangmanServer(port=1222)
    s.run()
    s.close()
