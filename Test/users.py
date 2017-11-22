#!/usr/bin/python
class User(object):
    def __init__(self,name=None):
        self.name = name


class Player(User):
    def __init__(self,name=None):
        super(Player,self).__init__(name)
        self.passwd = None
        self.score = 0
        self.guesses = 0

    def send(self,msg):
        print "Sent to", self.name, "\n",msg, "\n"

    def recv(self):
        d = raw_input("["+self.name+ "]: ")
        if d == "":
            return None
        else:
            return d

