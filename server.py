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

class HangmanServer(Server):
    def __init__(self, host='', port=2222):
        super(HangmanServer,self).__init__(host,port)
        #self.usersList = []
        self.players = []
        self.hallOfFameList = ["Tom", "Dick","Harry"]
        self.gamesList = [Hangman(name="HangmanA"), Hangman(name="HangmanB")]
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

    def process(self,player, playersList):
        #whle True
        while player in playersList:
            menu = ClientMenu(player=player, usersFilename="users.txt",
                              gameList=self.gamesList, 
                              hallOfFameList=self.hallOfFameList)
        
            player, gameChoice, difficulty = menu.run() 
            player.send("Done With Menu\n")
            #print("players name: ", player.name)
            #print("players addr: ", player.addr)
            #print("[!] Failed in Menu processing")

            #print("gameChoice: ", gameChoice.getName())
            print("gameChoice: ", gameChoice)
            #try:
            #if gameChoice.getName() not in [x.getName() for x in self.gamesList] :
            #create new game
            if gameChoice not in self.gamesList:
                print("[+] Creating New Game")
                #print "gameChoice in gamesList: ", gameChoice.name 
                hangman = Hangman(name=player.name)
                self.gamesList.append(hangman)
                #hangman.start()
                print("Playing: ", hangman.name)
                hangman.difficulty = difficulty
                hangman.add(player)
                active = hangman.play()
                """
                if not active:
                    #kill thread
                    hangman.join()
                """

            #join existing game
            else:
                #print("gameChoice: ", gameChoice.getName(), " NOT in gamesList")
                print("[+] Joining ", gameChoice)
                hangman = None
                for game in self.gamesList:
                    if game.name == gameChoice.name:
                        game.add(player)
                        hangman = game
                print("Playing: ", hangman.name)
                active = hangman.play()
                """
                if not active:
                    hangman.join()
                """
            #except:
            #print("[!] Failure in Game process")
                
                
    def run(self):
        print("[+] Welcome to the Hangman Server\n")
        while True:
            # wait to accept connection (blocking call)
            conn, addr = self.s.accept()
            player = Player(conn=conn,addr=addr)
            if player not in self.players:
                self.players.append(player)
           
            try: 
                #self.process(player,self.players)
                start_new_thread(self.process,(player,self.players))
            except:
                print("[!] Failed to create Thread")


if __name__ == "__main__":
    s = HangmanServer(port=1222)
    s.run()
    s.close()
