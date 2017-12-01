import threading

class GameThread(threading.Thread):
    def __init__(self,name,*args, **kwargs):
    #threading.Thread.__init__()
    self.playersList = []
    self.name = name

    def run(self):
        print "playersList: ", self.playersList

    def addPlayer(self, player):
        threadLock.acquire()
        self.playersList.append(player)

threadLock = threading.Lock()
plist = ["Tom", "Dick", "Harry", "Sally"]
g1 = GameThread("Game1")
g2 = GameThread("Game2")
g3 = GameThread("Game3")

