#!/usr/bin/python
from __future__ import print_function
import sys
from time import sleep
import threading

class Menu(object):
    def __init__(self):
        pass    
    def sendPrompt(self,data):
        raise NotImplementedError


class AdminMenu(object):
    def __init__(self,usersrepo,wordrepo, gameList, hallOfFameList):
        self.adminSplashScreen = "/"*17 + "\n" + "/"+ "Admin Menu".center(12) + "   /\n" +"/"*17 +"\n\n"
        self.adminScreen = "1.Get Current Users\n2.Get Current Words\n3.Add New Word\n"
        self.usersList = usersrepo.getData()
        self.active = True
        self.wordRepo = wordrepo
        self.gamesList = gameList
        self.request = {"admin":{1:self.getCurrentUsers,
                                 2:self.getCurrentWords,
                                 3:self.addWords
                                 }
                               }
    def sendPrompt(self,screen, resp=True):
        if resp == True:
            print(screen)
            return raw_input(">>")
        else:
            print(screen)

    def getCurrentUsers(self):
        msg = "[+] Current Users:\n"
        for name, _ in self.usersList:
            msg += str(name) +"\n"
        self.sendPrompt(msg,resp=False)
        
    def getCurrentWords(self):
        msg = "[+] Current Word List:\n" 
        words = self.wordRepo.getData()
        for word in words:
            msg += str(word) +"\n"
        self.sendPrompt(msg,resp=False)
            
    def addWords(self):
        msg = "[+] Enter word to Add\n"
        word = self.sendPrompt(msg)
        wordlist = self.wordRepo.getData()
        if word not in wordlist:
            print("wordlist: ", wordlist)
            wordlist.append(word)
            self.wordRepo.saveData(wordlist)        

    def run(self):
        # Admin Menu
        d = self.sendPrompt(self.adminSplashScreen +self.adminScreen)
        menu = "admin" 
        if d != "":
            if d.isdigit():
                if int(d) in self.request[menu].keys():
                    self.request[menu][int(d)]()
                else:
                    self.sendPrompt("[!] Invalid selection NOT in menu",resp=False)
                    sleep(0.25)
            else:
                self.sendPrompt("[!] Invalid selection NOT a digit",resp=False)
                sleep(0.25)
        return self.active
            


class ClientMenu(object):
    def __init__(self,usersrepo, wordrepo, player=None, gameList=[], hallOfFameList=[]):
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
        self.usersList = usersrepo.getData()
        self.request = {"main":{1:self.login,
                                2:self.makeUser,
                                3:self.hall,
                                4:self.exit },

                        "game":{1:self.difficulty,
                                2:self.getGamesList,   
                                3:self.hall,
                                4:self.exit}
                        }

    def login(self):
        username = self.sendPrompt("#" + self.loginScreen1)
        password = self.sendPrompt("#" + self.loginScreen2)
        #Authenticate Login
        if (username,password) not in self.usersList or "#" in username:
            self.conn.send("[!] Authentication Failed!\nPlease try again\n\n") 
            sleep(0.25)
            self.state = 1
            return self.state
        else:
            for user, paswd in self.usersList:
                if user == username and paswd == password:
                    msg = "[+] User: " + str(username) + " Authenticated!\n"
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
        top = []
        length = len(self.hallOfFameList)
        if x > length-1:
            x = length-1
        for i in range(length-1,length-x-1,-1):
            p = self.hallOfFameList[i]
            top.append(str(p[0]) +": " + str(p[1]))  
        return top

    def makeUser(self):
        username = self.sendPrompt("#" + self.loginScreen1)
        password = self.sendPrompt("#" + self.loginScreen2)
        for name, _ in self.usersList:
            if name == username:
                msg = "[+] OoOops!\nUsername Already taken try another one\n"
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
        msg = "***HALL OF FAME***\n"+"\n".join(self._getTop(3)) +"\n"+"*"*18+"\n"
        self.conn.send(msg) 
        sleep(0.25)
        return 1 
   
## END Main Menu ##

## Game Menu ##
    def getGamesList(self):
        g = [str(i+1)+"."+game.name+"\n" for i,game in enumerate(self.gamesList)]
        if len(g) ==0:
            self.conn.send("[+] No active games right now... Please Create one")
            self.state = 2
            return None 
        choice = self.sendPrompt("#" + "".join(g) +"\n")
        if choice != None and choice.isdigit():
            self.gameChoice = self.gamesList[int(choice)-1]
            self.conn.send(self.gameChoice.name + " selected!\n\n")
            self.state = 3
            return 1
        else:
            if not choice.isdigit():
                self.conn.send("[!] Invalid Games menu option: is Not a digit")
            else:
                self.conn.send("[!] Invalid Games menu option")
            return None

    def difficulty(self):
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
        return True

    def sendPrompt(self,screen,error=False):
        if error == False:
            self.conn.send(screen)
            d = self.conn.recv(1024)
            if d == "":
                print("in menu::sendPrompt: recved null string")
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
            
            # Admin Menu
            if self.state == 4:
                d = self.sendPrompt(self.adminSplashScreen +self.adminScreen)
                menu = "admin" 

            if d != "":
                if d.isdigit():
                    if int(d) in self.request[menu].keys():
                        self.request[menu][int(d)]()
                    else:
                        self.conn.send("[!] Invalid selection NOT in menu")
                        sleep(0.25)
                else:
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
        
