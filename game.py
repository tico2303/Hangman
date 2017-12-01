#!/usr/bin/python
from __future__ import print_function
import random
from users import Player
from os import system
from words import wordlist
import threading

<<<<<<< HEAD
class ThreadedHangman(threading.Thread):
    def __init__(self, name,playersList=[],*args, **kwargs):
        super(ThreadedHangman, self).__init__()
        self.playersList = playersList
        self.hangman = Hangman(name,self.playersList)
        
=======
>>>>>>> temp

class Game(object):
#class Game(threading.Thread):
    def __init__(self, name,*args, **kwargs):
<<<<<<< HEAD
        #super(Game, self).__init__()
        self.playersList_lock = threading.Lock()
=======
>>>>>>> temp
        self.difficulty = 1
        self.name = name + str(random.randint(0,10000))
        self.active = False

    def play(self):
        raise NotImplementedError

class Hangman(Game):
    def __init__(self,wordrepo,name=None, playersList=[], *args, **kwargs):
        super(Hangman,self).__init__(name,*args, **kwargs) 
        self.wordList = wordrepo.getData() 
        self.playersList = playersList
        self.solution = {}
        self.guesses = []
        self.word = None
        self.wordRepo = wordrepo
        self.turn = 0
        self.newGame = True
        self.puzzleCenter = 40
        self.beginSplash = "*******************\n"
        self.bannerSplash = "*" + "HangMan".center(17) + "*\n"
        self.gameNameSplash = "*" + self.name.center(17) + "*\n"
        self.endSplash = "*******************\n\n\n"
    
    def __str__(self):
        return repr(self) + "GameName:" +self.name + ", PlayersList: [" +" ".join([p.name for p in self.playersList]) + "]"

    def add(self,player):
        print("[+] Player: ", player.name, " joined the Game!")
        if player not in self.playersList:
            self.playersList.append(player)

    def remove(self,player):
        for i, user in enumerate(self.playersList):
            if user.name == player.name:
                del self.playersList[i]
                break

    def addWord(self,word):
        if word not in self.wordList:
            self.wordList.append(word)        

    def getRandomWord(self):
        return random.choice(self.wordList)         

    def isPuzzleSolved(self):
        if "_" not in self.puzzle:
            return True
        else:
            return False

    def isMaxGuesses(self):
        if len(self.guesses) >= (len(self.word) * (4-int(self.difficulty))):
            return True
        else:   
            return False

    def guessLetter(self, player, letter):
        print("[+] Guessing letter")
        correct = False
        self.guesses.append(letter)
        for index,ch in enumerate(self.word):
            if ch == letter and self.puzzle[index] != self.solution[index]: 
                self.puzzle[index] = self.solution[index]
                player.score +=1 
                correct = True
        return correct

    def guessWord(self, player, word):
        if word.lower() == self.word.lower():
            player.score += len(self.word)
            self.puzzle = self.word
            return True
        else:
            return False

    def guess(self,player,guess):
        if len(guess) <= 1:
            correct = self.guessLetter(player, guess)
        else:
            correct = self.guessWord(player,guess)
            if not correct:
                print("[+] Incorrect Word Guess.. removing: ", player.name)
                self.remove(player)
        return correct

    def setup(self):
        print("[+] Setting up hangman game")
        self.word = self.getRandomWord()
        self.puzzle = [ "_" for i in range(len(self.word))]
        for index, letter in enumerate(self.word):
            self.solution[index] = letter

    def nextPlayer(self):
        print("[+] Getting next player")
        if self.newGame:
            self.turn = 0
<<<<<<< HEAD
            self.newGame = False
        else:
            self.turn +=1

        if self.playersList:
            print("turn index: ", self.turn%(len(self.playersList)))
            self.turn = self.turn %(len(self.playersList))
            player = self.playersList[self.turn]         
            print("player at turn index: ", player.name)
            print("playersList: ", [p.name for p in self.playersList])
            return player
        return None
=======
        else:
            self.turn += 1 

        #print("turn index: ", self.turn%(len(self.playersList)))
        self.turn = self.turn %(len(self.playersList))
        player = self.playersList[self.turn]         
        print("player turn is: ", player.name)
        #print("playersList: ", [p.name for p in self.playersList])
        return player
>>>>>>> temp

    def showPuzzle(self):
        #print("[+] Showing Puzzle")
        return " ".join(self.puzzle).center(self.puzzleCenter) + "\n\n"

    def showPlayers(self):
        #print("[+] Showing players")
        display = []
        for i, player in enumerate(self.playersList):
            if i == self.turn%(len(self.playersList)):
                display.append(player.name +": "+str(player.score)+ " *\n")
            else:
                display.append(player.name +": "+str(player.score)+ "\n")
        return " ".join(display)+"\n"

    def showGuesses(self):
        #print("[+] Showing Guesses")
        return " ".join(self.guesses) + "\n\n\n"

    def showBoard(self):
        #print("[+] Showing Board to: ", self.playersList[self.turn%(len(self.playersList))])        
        banner = self.beginSplash + self.bannerSplash +self.gameNameSplash + self.endSplash
        board = banner + self.showPuzzle() +  self.showGuesses()+ self.showPlayers() 
        return board

    def broadCastBoard(self, playerturn=None,):
        print("[+] Boardcasting Board")
        #print("@ boardCast playersList is: ",self.playersList)
        for player in self.playersList:
<<<<<<< HEAD
            player.send(self.showBoard())

=======
            if player == playerturn:
                player.send("#" + self.showBoard())
            else:
                player.send(self.showBoard())
            
>>>>>>> temp
    def broadCastExclusive(self,player,msg):
        if player == None:
            for p in self.playersList:
                p.send(msg)
        else:
            for p in self.playersList:
                if p != player:
                    p.send(msg)

    def printPlayers(self):
        for players in self.playersList:
            print(players.name ,", " )

    def play(self):
        if self.newGame:
<<<<<<< HEAD
            print("[+] New Game Created!")
            self.setup()             
            self.active = True
        print("[+] Starting Game loop")
        while not self.isPuzzleSolved() or not self.isMaxGuesses():
            player = self.nextPlayer() 
            print("player: ", player)
            if player:
                self.broadCastBoard()
                guess = player.recv()
                correct = self.guess(player,guess)
            else:
                break
=======
            self.setup()
            self.newGame = False
        self.active = True
        print("[+] Starting Game loop")

        while not self.isPuzzleSolved() and not self.isMaxGuesses():
            print("[~] Current PlayersList: ", self.printPlayers())
            #print("[~] iPuzzleSolved: ", self.isPuzzleSolved())
            #print("[~] isMaxGuesses: ", self.isMaxGuesses())
            player = self.nextPlayer()
            #print("Current player: ", player.name, " 's turn")
            self.broadCastBoard(playerturn=player)
            #player.send("#" + "It's your turn " + player.name + "\n")
            #print("calling player.recv")
            guess = player.recv()
            #print(player.name, "'s guess is: ", guess)
            correct = self.guess(player,guess)
            #print("[~] correct: ", correct)
>>>>>>> temp
            # keep guessing until you have a wrong answer, puzzle is solved or max guesses is reached
            while correct and not self.isPuzzleSolved() and not self.isMaxGuesses():
                #print("[+] In correct Guess Loop")
                self.broadCastBoard(playerturn=player)
                guess = player.recv()
                correct = self.guess(player,guess)
                if not correct:
                    break

        if self.isPuzzleSolved():
            print("[+] ", self.name, " was solved by ", player.name, "!")
            self.broadCastBoard()
            player.send(str(player.name) +" YOU WON!\n\n")
            self.broadCastExclusive(player,"You Lost\n\n")
            self.active = False
            return self.active 
        else:
            self.broadCastBoard()
            self.broadCastExclusive(None, "You Lost\n\n")
            self.active = False
            return self.active
    
            
if __name__ == "__main__":
    from users import Player

    hangman = Hangman(name="TestGame")
    playerList = []  
    for player in ["Tom", "Dick","Harry"]:
        p = Player("conn", "addr", name=player) 
        playerList.append(p) 
        hangman.add(p)     
    #hangman.playersList = playerList
    print("hangman playersList: ", hangman.playersList)
    hangman.play()


