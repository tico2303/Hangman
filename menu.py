#!/usr/bin/python
from __future__ import print_function
import sys
from time import sleep
import threading

class ClientMenu(object):
    def __init__(self,usersrepo, wordrepo, player=None, gameList=[], hallOfFameList=[]):
        #self.conn = conn
        self.conn = player.conn
        self.difficultyLevel = 0
        self.player = player
        self.username = None
        self.password = None
        self.gamesList = gameList
        self.hallOfFameList = hallOfFameList
        self.usersRepo = usersrepo
        self.wordRepo = wordrepo
        self.gameChoice = None
        self.mainScreen ="1.Login\n2.Make New User\n3.Hall of fame\n4.Exit\n"
        self.loginScreen1 = "What is your user name?\n" 
        self.loginScreen2 = "What is your user password?\n"
        self.gamesScreen = "1.Start New Game\n2.Get list of Games\n3.Hall of Fame\n4.exit\n"
        self.difficultyScreen = "Choose the difficulty:\n1.Easy\n2.Medium\n3.Hard\n"
        self.adminSplashScreen = "#"+"/"*17 + "\n" + "/"+ "Admin Menu".center(12) + "   /\n" +"/"*17 +"\n\n"
        self.adminScreen = "1.Get Current Users\n2.Get Current Words\n3.Add New Word\n4.Exit\n"
        self.usersList = usersrepo.getData()
        self.request = {"main":{1:self.login,
                                2:self.makeUser,
                                3:self.hall,
                                4:self.exit },

                        "game":{1:self.difficulty,
                                2:self.getGamesList,   
                                3:self.hall,
                                4:self.exit},

                        "admin":{1:self.getCurrentUsers,
                                 2:self.getCurrentWords,
                                 3:self.addWords,
                                 4:self.exit}
                               }
## Admin Menu ##
    def getCurrentUsers(self):
        #msg = self.adminSplashScreen
        msg = "#[+] Current Users:\n"
        #print("usersList: ", self.usersList)
        for name, _ in self.usersList:
            msg += str(name) +"\n"
        msg +="\nEnter ANY number to return to menu\n"
        #self.conn.send(msg)
        self.sendPrompt(msg)
        #sleep(0.25)
        
    def getCurrentWords(self):
        msg = "#[+] Current Word List:\n" 
        words = self.wordRepo.getData()
        #print("words: ", words)
        for word in words:
            msg += str(word) +"\n"
        msg +="\nEnter ANY number to return to menu\n"
        #self.conn.send(msg)
        self.sendPrompt(msg)
        #sleep(0.25)
            
    def addWords(self):
        #msg = self.adminSplashScreen
        msg = "[+] Enter word to Add\n"
        word = self.sendPrompt("#" + msg)
        wordlist = self.wordRepo.getData()
        #print("wordList: ", wordlist)
        if word not in wordlist:
            print("wordlist: ", wordlist)
            wordlist.append(word)
            self.wordRepo.saveData(wordlist)        

## END Admin Menu ##         

## Main Menu ##
    def login(self):
        print("[+] Processing Login")
        username = self.sendPrompt("#" + self.loginScreen1)
        password = self.sendPrompt("#" + self.loginScreen2)
        #Authenticate Login
        if (username,password) not in self.usersList:
            print("[!] Authentication Failed!")
            self.conn.send("[!] Authentication Failed!\nPlease try again\n\n") 
            sleep(0.25)
            self.state = 1
            return self.state
        else:
            for user, paswd in self.usersList:
                if user == username and paswd == password:
                    msg = "[+] User: " + str(username) + " Authenticated!\n"
                    print(msg)
                    self.conn.send(msg)
                    sleep(0.25)
                    self.player.name = username 
                    self.player.passwd = password
                    self.username = username
                    self.password = password
                    if self.username == "Admin":
                        self.state = 4
                    else:
                        self.state = 2
                    return self.state

    def _getTop(self,x):
        print("[+] Getting top ", x, " Hall-of-Famers")
        top = []
        if x > len(self.hallOfFameList)-1:
            x = len(self.hallOfFameList)-1
        for i in range(x,-1,-1):
            p = self.hallOfFameList[i]
            top.append(str(p[0]) +": " + str(p[1]))  
        return top

    def makeUser(self):
        print("[+] Making User...")
        username = self.sendPrompt("#" + self.loginScreen1)
        password = self.sendPrompt("#" + self.loginScreen2)
        for name, _ in self.usersList:
            if name == username:
                msg = "[+] OoOops!\nUsername Already taken try another one\n"
                print(msg)
                self.conn.send(msg)
                sleep(0.25)
                return None
        self.player.name = username 
        self.player.passwd = password
        self.username = username
        self.password = password
        creds = (username, password)
        self.usersList.append(creds)
        self.usersRepo.saveData(self.usersList) 
        self.state =2
        return self.state

    def hall(self):
        print("[+] Retrieving Hall of Fame...")
        msg = "***HALL OF FAME***\n"+"\n".join(self._getTop(3)) +"\n"+"*"*18+"\n"
        #self.sendPrompt(msg)
        self.conn.send(msg) 
        sleep(0.2)
        return 1 
   
## END Main Menu ##

## Game Menu ##
    def getGamesList(self):
        print("[+] Serving Games List...")
        g = [str(i+1)+"."+game.name+"\n" for i,game in enumerate(self.gamesList)]
        if len(g) ==0:
            print("[+] Game list Empty")
            self.conn.send("[+] No active games right now... Please Create one")
            self.state = 2
            return None 
        choice = self.sendPrompt("#" + "".join(g) +"\n")
        if choice != None and choice.isdigit():
            self.gameChoice = self.gamesList[int(choice)-1]
            self.conn.send(self.gameChoice.name + " selected!\n\n")
            self.difficulty()
            return 1
        else:
            if not choice.isdigit():
                print("[!] Invalid Games menu option: is Not a digit")
                self.conn.send("[!] Invalid Games menu option: is Not a digit")
            else:
                print("[!] Invalid Games menu option")
                self.conn.send("[!] Invalid Games menu option")
            return None

    def difficulty(self):
        print("[+] Setting Difficulty Level...")
        self.difficultyLevel = self.sendPrompt("#" +self.difficultyScreen)
        self.state = 3
        return self.state

    def exit(self):
        print("[+] Closing Connection and exiting...")
        sleep(0.25)
        self.conn.send("q!")
        self.conn.close()
        """
        for t in threading.enumerate():
            print t.getName()
            print("\n")
        """
        print("[+] Connection closed")
        sys.exit()
    ######### END Menu Option Responses ############

    def isValid(self,resp):
        if resp == "":
            return False

    def sendPrompt(self,screen,error=False):
        if error == False:
            self.conn.send(screen)
            d = self.conn.recv(1024)
            if d == "":
                return None
            return d
        else:
            self.conn.send(screen)
            
            
    def run(self):
        self.state = 1
        while True:
            # Main Menu
            if self.state == 1:
                d = self.sendPrompt("#"+self.mainScreen)
                menu = "main"

            # Start Game menu
            if self.state == 2:
                d = self.sendPrompt("#"+ self.gamesScreen )     
                menu = "game"
            
            
            # return to play Game
            if self.state == 3:
                return (self.player,self.gameChoice, self.difficultyLevel)
                #return (self.username, self.gameChoice, self.difficultyLevel)
            
            # Admin Menu
            if self.state == 4:
                d = self.sendPrompt(self.adminSplashScreen +self.adminScreen)
                menu = "admin" 

            if d != "":
                if d.isdigit():
                    print(d)
                    print ("keys: ", self.request[menu].keys())
                    if int(d) in self.request[menu].keys():
                        print(d, "is in request menu!")
                        self.request[menu][int(d)]()
                    else:
                        print("[!] invalid selection NOT in menu")
                        self.conn.send("[!] Invalid selection NOT in menu")
                        sleep(0.25)
                else:
                    print("[!] invalid selection NOT a digit")
                    self.conn.send("[!] Invalid selection NOT a digit")
                    sleep(0.25)

    def print_state(self):
        print("username: ", self.username )
        print("passwd: ", self.passwd)
        print("difficulty level: ", self.difficulty)
        print("gameList flag: ",self.gameList)
        print("hallOfFame flag: ",self.hallOfFame)
         

if __name__ == "__main__":
    pass
        
