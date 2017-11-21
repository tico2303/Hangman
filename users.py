#!/usr/bin/python
class User(object):
    def __init__(self,conn, addr,name=None):
        self.name = name
        self.conn = conn
        self.addr = addr


class Player(User):
    def __init__(self,conn,addr,name=None):
        super(Player,self).__init__(conn,addr,name)
        self.passwd = None
        self.score = 0
        self.guesses = 0

    def send(self,msg):
        self.conn.send(msg)

    def recv(self):
        d = self.conn.recv(4096)
        if d == "":
            return None
        else:
            return d

