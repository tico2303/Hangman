#!/usr/bin/python
import sys

class ClientMenu(object):
    def __init__(self,usersFilename,player, gameList=[], hallOfFameList=[]):
        self.conn = player.conn
        self.difficultyLevel = 0
        self.player = player
        self.gamesList = gameList
        self.hallOfFameList = hallOfFameList
        self.usersFilename = usersFilename
        self.gameChoice = None
        self.mainScreen ="1.Login\n2.Make New User\n3.Hall of fame\n4.Exit\n"
        self.loginScreen1 = "What is your user name?\n" 
        self.loginScreen2 = "What is your user password?\n"
        self.gamesScreen = "1.Start New Game\n2.Get list of Games\n3.Hall of Fame\n4.exit\n"
        self.difficultyScreen = "Choose the difficulty:\n1.Easy\n2.Medium\n3.Hard\n"
        self.usersList = []
        self._populateData()
        
        
        self.request = {"main":{1:self.login,
                                2:self.makeUser,
                                3:self.hall,
                                4:self.exit },

                        "game":{1:self.difficulty,
                                2:self.getGamesList,   
                                3:self.hall,
                                4:self.exit},
                               }
         
    def _populateData(self):
        f = open(self.usersFilename,'r')
        for user in f.readlines():
            user,paswd = user.strip().split(" ") 
            self.usersList.append((user,paswd))
        f.close()
    
    def login(self):
        print("[+] Processing Login")
        username = self.sendPrompt(self.loginScreen1)
        password = self.sendPrompt(self.loginScreen2)
        if username != None and password != None:
            #Authenticate Login
            for user, paswd in self.usersList:
                if user == username and paswd == password:
                    print("[+] User: ", username, " Authenticated!")
                    self.player.name = username 
                    self.player.passwd = password
                    self.state = 2
                    return self.state
        else:
            print("[!]Authentication Failed!")
            self.sendPrompt("[!]Authentication Failed!\n\n", error=True)
            self.state = 1
            return self.state

    def hall(self):
        print("[+] Retrieving Hall of Fame...")
        msg = "***HALL OF FAME***\n"+"\n".join(self.hallOfFameList) +"\n"+"*"*18+"\n"
        self.conn.send(msg) 
        return 1 
    
    def makeUser(self):
        print("[+] Making User...")
        f = open(self.usersFilename, 'a')
        username = self.sendPrompt(self.loginScreen1)
        password = self.sendPrompt(self.loginScreen2)
        if username != None and password != None:
            self.player.name = username 
            self.player.passwd = password
            creds = username + " " + password + "\n" 
            f.write(creds)
            f.close()
            self.state =2
        else:
            print("[!] Make User Failed")
            self.sendPrompt("[!] Make User Failed Try again", error=True)
        return self.state
   
    def getGamesList(self):
        print("[+] Serving Games List...")
        g = [str(i+1)+"."+game.name+"\n" for i,game in enumerate(self.gamesList)]
        choice = self.sendPrompt("".join(g) +"\n")
        if choice != None:
            self.gameChoice = self.gamesList[int(choice)-1]
            self.conn.send(self.gameChoice.name + " selected!\n\n")
            #self.conn.send(self.gameChoice.getName() + " selected!\n\n")
            self.difficulty()
            return 1
        else:
            print("[!] Invalid Games menu option")

    def difficulty(self):
        print("[+] Setting Difficulty Level...")
        self.difficultyLevel = self.sendPrompt(self.difficultyScreen)
        self.state = 3
        return self.state

    def exit(self):
        print("[+] Closing Connection and exiting...")
        self.conn.close()
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
                d = self.sendPrompt(self.mainScreen)
                menu = "main"

            # Start Game menu
            if self.state == 2:
                d = self.sendPrompt(self.gamesScreen )     
                """
                if int(d) == 2:
                    self.state =4
                """
                menu = "game"
            
            # return to play Game
            #if self.state == 4:
                
            if self.state == 3:
                return (self.player,self.gameChoice, self.difficultyLevel)

            #print("state: ", self.state)            
            #print("menu: ", menu)
            #print("d: ", d)
            if d != "":
                if d.isdigit():
                    self.request[menu][int(d)]()

    def print_state(self):
        print("username: ", self.username )
        print("passwd: ", self.passwd)
        print("difficulty level: ", self.difficulty)
        print("gameList flag: ",self.gameList)
        print("hallOfFame flag: ",self.hallOfFame)
         

if __name__ == "__main__":
    pass
        
