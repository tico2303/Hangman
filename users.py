
class User(object):
    def __init__(self,name,conn):
        self.name = name
        self.passwd = None
        self.conn = conn



class Player(User):
    def __init__(self,name,conn):
        super(Player,self).__init__(name,conn)
        self.score = 0
        self.guesses = 0

