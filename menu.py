import sys

class ClientMenu(object):
    def __init__(self):
        self.username = None
        self.passwd = None
        self.newUser = str(False)
        self.difficulty = 0
        self.newGame = str(False)
        self.gameList = str(False)
        self.hallOfFame = str(False)
        
    def mainMenu(self):
        screen = "1.Login\n2.Make New User\n3.Hall of fame\n4.Exit\n"
        resp = int(raw_input(screen))
        if resp == 1:
            self.newUser = str(False)
            return self.login()
            
        elif resp == 2:
            self.newUser = str(True)
            return self.makeUser()

        elif resp == 3:
            self.hallOfFame = str(True)
            return self.hall("menu")

        elif resp == 4:
            self.exit()
            return 4

        else:
            print("Please select a number\n")
            self.mainMenu()
    
    def hall(self,menu):
        return ["hall",menu ]

    def login(self):
        screen1 = "What is your user name?\n" 
        screen2 = "What is your user password?\n"
        self.username = raw_input(screen1) 
        self.passwd = raw_input(screen2) 
        return ["login",self.username, self.passwd]

    def makeUser(self):
        screen1 = "What is your user name?\n" 
        screen2 = "What is your user password?\n"
        self.username = raw_input(screen1) 
        self.passwd = raw_input(screen2) 
        return ["makeUser",self.username, self.passwd]

    def games(self):
        self.newGame = str(False)
        self.hallOfFame = str(False)
        self.gameList = str(False)
        while True:
            screen = "1.Start New Game\n2.Get list of Games\n3.Hall of Fame\n4.exit\n"
            resp = int(raw_input(screen))
            if resp in [1,2,3,4]:    
                if resp == 1:
                    self.newGame = str(True)
                    return ["games",self.newGame, self.gameList, self.hallOfFame]
                if resp == 2:
                    self.gameList = str(True)
                    return ["games",self.newGame, self.gameList, self.hallOfFame]
                if resp == 3:
                    self.hallOfFame = str(True)
                    return self.hall("game")
                if resp == 4:
                    self.mainMenu()
                    return ["games",None, None, None]
                         
            else:
                print("Please select a number")
            
    def difficultyMenu(self):
        screen = "Choose the difficulty:\n1.Easy\n2.Medium\n3.Hard\n"
        resp = int(raw_input(screen))
        if resp in [1,2,3]:    
            self.difficulty = resp    
            return ["difficulty",str(self.difficulty)]
        else:
            print("Please select a number")
            self.difficultyMenu()

    def exit(self):
        sys.exit() 

    def print_state(self):
        print("username: ", self.username )
        print("passwd: ", self.passwd)
        print("newUser flag: ", self.newUser )
        print("difficulty level: ", self.difficulty)
        print("newGame flag: ",self.newGame)
        print("gameList flag: ",self.gameList)
        print("hallOfFame flag: ",self.hallOfFame)
         
    def run(self):
        self.mainMenu() 

if __name__ == "__main__":

    menu = ClientMenu()
    print menu.mainMenu()
    #menu.print_state()

    print("calling games")
    print menu.games()
    #menu.print_state()

    print("calling difficulty")
    print menu.difficultyMenu()
    #menu.print_state()
        
