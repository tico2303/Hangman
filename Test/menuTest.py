from time import sleep

class Users(object):
    def __init__(self):
        self.name = None
        self.conn = None
        self.score = None
        self.addr = None

class GameTest(object):
    def __init__(self):
        self.dataList = []
        self.data = None
        self.playerList = []
    
    def addPlayer(self, player):
        if player not in self.playerList:
            self.playerList.append(player)
   
    def showPlayers(self):
        for p in self.playerList:
            print p.name 

    def run(self):
        while True:
            print("dataList: ", self.dataList)
            print("data: ", self.data)
            print("self.playersList: ", self.showPlayers())
            for p in self.playerList:
                p.conn.send("dataList: "+ " ".join(self.dataList))
            sleep(3) 
