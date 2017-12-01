#!/usr/bin/python
from __future__ import print_function
import socket
import threading
from thread import start_new_thread
import sys
from menu import ClientMenu
from users import Player
from game import Hangman
from repo import *

class Server(object):
    def __init__(self, host='', port=2222):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error, msg:
            print("Socket creation failed")
        self.host = host
        self.port = port 
        try:
            self.s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
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
    def __init__(self, hofrepo, usersrepo,wordrepo, host='', port=2222):
        super(HangmanServer,self).__init__(host,port)
        self.players = []
<<<<<<< HEAD
        self.hallOfFameList = ["Tom", "Dick","Harry"]
        self.gamesList = [Hangman(name="HangmanA"), Hangman(name="HangmanB")]
        self.gameDict = {}
        #self._populateData()
=======
        self.hallOfFameList = hofrepo.getData()
        self.hallOfFameDict = {}
        self.hofRepo = hofrepo
        self.usersRepo = usersrepo
        self.wordRepo = wordrepo
        self.gamesList = []
        self.activeGame = {}
        self.hallLock = threading.Lock()
        self.menuLock = threading.Lock()
    
>>>>>>> temp

    def updateHallofFame(self,player):
        self.hallLock.acquire()

<<<<<<< HEAD
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
=======
        if player.name in dict(self.hallOfFameList): 
            for i, (name, score) in enumerate(self.hallOfFameList):
                if name == player.name:
                    print("[+] Updating hallOfFameList")
                    self.hallOfFameList[i] = (player.name, player.score +score)    
        else:
            self.hallOfFameList.append((player.name, player.score))        
>>>>>>> temp

        self.hallOfFameList.sort(key=lambda x:x[1])        
        self.hofRepo.saveData(self.hallOfFameList)
        self.hallLock.release()
        player.score = 0
        
    def menu(self, player):
            self.menuLock.acquire()
            menu = ClientMenu(player=player, usersrepo=self.usersRepo,
                              gameList=self.gamesList, 
                              hallOfFameList=self.hallOfFameList,
                              wordrepo=self.wordRepo)
            self.menuLock.release()
            player, gameChoice, difficulty = menu.run() 
<<<<<<< HEAD
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
=======
            self.process(player, gameChoice, difficulty)

    def process(self, player, gameChoice, difficulty ):

            #Create New Game
            if gameChoice not in self.gamesList:
                print("[+] Creating New Game")
                hangman = Hangman(name=player.name, wordrepo=self.wordRepo)
                self.gamesList.append(hangman)
>>>>>>> temp
                hangman.difficulty = difficulty
                hangman.add(player)
                for p in hangman.playersList:
                    if p != player:
                        hangman.playersList.remove(p)
                active = hangman.play()
<<<<<<< HEAD

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
=======
                hangman.playersList = []
                self.gamesList.remove(hangman)
                self.updateHallofFame(player)
                self.menu(player)
                                
            #Join Existing Game
            else:
                if gameChoice != None:
                    print("[+] ", player.name, " Joining ", gameChoice.name)
                    hangman = None
                    for game in self.gamesList:
                        if game.name == gameChoice.name:
                            if player not in game.playersList:
                                print("Adding player: ", player.name, " to ", game.name)
                                game.add(player)
                                hangman = game

                    player.send("[+] Waiting to join game...")
                    # while the game is active (playing) stay in while loop
                    while hangman.active:
                        pass
                    self.updateHallofFame(player)
                    self.menu(player)

                
    def run(self):
        print("[+] The Hangman Server\n")
>>>>>>> temp
        while True:
            # wait to accept connection (blocking call)
            conn, addr = self.s.accept()
            player = Player(conn=conn,addr=addr)
            player.send("[+] Welcome to the Hangman Server\n\n")
            if player.addr not in [p.addr for p in self.players]:
                self.players.append(player)
           
            try: 
<<<<<<< HEAD
                #self.process(player,self.players)
                t = threading.Thread(target=self.process,args=(player,self.players))
                t.daemon = True
                t.start()
=======
                t = threading.Thread(target=self.menu, args=(player,))
                t.setName(str(conn))
                t.daemon = True
                t.start()
                #start_new_thread(self.process,(player,self.players))
>>>>>>> temp
            except:
                print("[!] Failed to create Thread")


if __name__ == "__main__":
    hofrepo = HallofFameRepo("hofDB.pkl")
    usersrepo = UsersRepo("usersDB.pkl")
    wordrepo = WordRepo("wordsDB.pkl")
    s = HangmanServer(port=2222,hofrepo=hofrepo,wordrepo=wordrepo, usersrepo=usersrepo)
    s.run()
