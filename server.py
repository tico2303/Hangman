#!/usr/bin/python
from __future__ import print_function
import socket
import threading
from thread import start_new_thread
import sys
from menu import ClientMenu
from menu import AdminMenu
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
        self.hallOfFameList = hofrepo.getData()
        self.hallOfFameDict = {}
        self.hofRepo = hofrepo
        self.usersRepo = usersrepo
        self.wordRepo = wordrepo
        self.gamesList = []
        self.activeGame = {}
        self.hallLock = threading.Lock()
        self.menuLock = threading.Lock()
    

    def updateHallofFame(self,player):
        self.hallLock.acquire()

        if player.name in dict(self.hallOfFameList): 
            for i, (name, score) in enumerate(self.hallOfFameList):
                if name == player.name:
                    #print("[+] Updating hallOfFameList")
                    self.hallOfFameList[i] = (player.name, player.score +score)    
        else:
            self.hallOfFameList.append((player.name, player.score))        

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
            self.process(player, gameChoice, difficulty)

    def process(self, player, gameChoice, difficulty ):

            #Create New Game
            if gameChoice not in self.gamesList:
                #print("[+] Creating New Game")
                hangman = Hangman(name=player.name, wordrepo=self.wordRepo)
                self.gamesList.append(hangman)
                hangman.difficulty = difficulty
                hangman.add(player)
                for p in hangman.playersList:
                    if p != player:
                        hangman.playersList.remove(p)
                active = hangman.play()
                hangman.playersList = []
                self.gamesList.remove(hangman)
                self.updateHallofFame(player)
                self.menu(player)
                                
            #Join Existing Game
            else:
                if gameChoice != None:
                    #print("[+] ", player.name, " Joining ", gameChoice.name)
                    hangman = None
                    for game in self.gamesList:
                        if game.name == gameChoice.name:
                            if player not in game.playersList:
                                #print("Adding player: ", player.name, " to ", game.name)
                                game.add(player)
                                hangman = game

                    player.send("[+] Waiting to join game...")
                    # while the game is active (playing) stay in while loop
                    while hangman.active:
                        pass
                    self.updateHallofFame(player)
                    self.menu(player)

                
    def run(self):
        #print("[+] The Hangman Server\n")
        while True:
            # wait to accept connection (blocking call)
            conn, addr = self.s.accept()
            player = Player(conn=conn,addr=addr)
            player.send("[+] Welcome to the Hangman Server\n\n")
            if player.addr not in [p.addr for p in self.players]:
                self.players.append(player)
           
            try: 
                t = threading.Thread(target=self.menu, args=(player,))
                t.setName(str(conn))
                t.daemon = True
                t.start()
                #start_new_thread(self.process,(player,self.players))
            except:
                pass
                #print("[!] Failed to create Thread")

    def serverMenu(self):
        active = True
        while active:
            servermenu = AdminMenu(usersrepo=self.usersRepo, wordrepo=self.wordRepo,
                                    gameList=self.gamesList, hallOfFameList=self.hallOfFameList)            
            active = servermenu.run()
        print("[+] Exing Admin Menu")
        sys.exit()

if __name__ == "__main__":
    hofrepo = HallofFameRepo("hofDB.pkl")
    usersrepo = UsersRepo("usersDB.pkl")
    wordrepo = WordRepo("wordsDB.pkl")


    hangmanS = HangmanServer(port=1222,hofrepo=hofrepo,wordrepo=wordrepo, usersrepo=usersrepo)
    t = threading.Thread(target=hangmanS.serverMenu,args=())
    t.daemon = True
    t.start()
    hangmanS.run()


