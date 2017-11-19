import sys

class ClientMenu(object):
    def __init__(self,usersFilename, conn,gameList=[], hallOfFameList=[]):
        self.conn = conn
        self.username = None
        self.passwd = None
        self.difficultyLevel = 0
        self.gamesList =gameList
        self.hallOfFameList = hallOfFameList
        self.usersFilename = usersFilename
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
                                4:self.exit}
                               }
         

    def _populateData(self):
        f = open(self.usersFilename,'r')
        for user in f.readlines():
            user,paswd = user.strip().split(" ") 
            self.usersList.append((user,paswd))
        f.close()
    
    def login(self):
        print("Processing Login")
        self.username = self.sendPrompt(self.loginScreen1)
        password = self.sendPrompt(self.loginScreen2)
        #Authenticate Login
        for user, paswd in self.usersList:
            if user == self.username and paswd == password:
                print("User: ", self.username, " Authenticated!")
                self.state = 2
                return self.state
        print("[!]Authentication Failed!")
        self.state = 1
        return self.state

    def hall(self):
        print("Retrieving Hall of Fame...")
        msg = "***HALL OF FAME***\n"+"\n".join(self.hallOfFameList) +"\n"+"*"*18+"\n"
        self.conn.send(msg) 
        return 1 
    
    def makeUser(self):
        print("Making User...")
        f = open(self.usersFilename, 'a')
        username = self.sendPrompt(self.loginScreen1)
        password = self.sendPrompt(self.loginScreen2)
        creds = username + " " + password + "\n" 
        f.write(creds)
        f.close()
        self.state =2
        return self.state
   
    def getGamesList(self):
        print("Retrieving Games List...")
        self.conn.send(" ".join(self.gamesList)+"\n")      

    def difficulty(self):
        self.difficultyLevel = self.sendPrompt(self.difficultyScreen)
        self.state = 3
        return self.state

    def exit(self):
        print("create exiting...")
    ######### END Menu Option Responses ############

    def sendPrompt(self,screen):
        self.conn.send(screen)
        d = self.conn.recv(1024)
        if d == "":
            return None
        return d
            
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
                menu = "game"

            # return to play Game
            if self.state == 3:
                return (self.conn, self.username,self.difficultyLevel)

            #print("state: ", self.state)            
            #print("menu: ", menu)
            #print("d: ", d)
            if d.isdigit():
                self.request[menu][int(d)]()

    def print_state(self):
        print("username: ", self.username )
        print("passwd: ", self.passwd)
        #print("newUser flag: ", self.newUser )
        #print("difficulty level: ", self.difficulty)
        #print("newGame flag: ",self.newGame)
        print("gameList flag: ",self.gameList)
        print("hallOfFame flag: ",self.hallOfFame)
         

if __name__ == "__main__":
    pass
        
