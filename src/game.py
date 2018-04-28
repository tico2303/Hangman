#!/usr/bin/python
from __future__ import print_function
import random
from users import Player
from os import system
from words import wordlist
import threading


class Game(object):
    def __init__(self, name,*args, **kwargs):
        self.difficulty = 1
        self.name = name + str(random.randint(0,10000))
        self.active = False

    def play(self):
        raise NotImplementedError

    def add(self,player):
        raise NotImplementedError
    
    def remove(self,player):
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
                self.remove(player)
        return correct

    def setup(self):
        self.word = self.getRandomWord()
        self.puzzle = [ "_" for i in range(len(self.word))]
        for index, letter in enumerate(self.word):
            self.solution[index] = letter

    def nextPlayer(self):
        if self.newGame:
            self.turn = 0
        else:
            self.turn += 1 
        if len(self.playersList) >= 1:
            self.turn = self.turn %(len(self.playersList))
            player = self.playersList[self.turn]         
            return player
        #no players
        else:
            return None 

    def showPuzzle(self):
        return " ".join(self.puzzle).center(self.puzzleCenter) + "\n\n"

    def showPlayers(self):
        display = []
        for i, player in enumerate(self.playersList):
            if i == self.turn%(len(self.playersList)):
                display.append(player.name +": "+str(player.score)+ " *\n")
            else:
                display.append(player.name +": "+str(player.score)+ "\n")
        return " ".join(display)+"\n"

    def showGuesses(self):
        return " ".join(self.guesses) + "\n\n\n"

    def showBoard(self):
        banner = self.beginSplash + self.bannerSplash +self.gameNameSplash + self.endSplash
        board = banner + self.showPuzzle() +  self.showGuesses()+ self.showPlayers() 
        return board

    def broadCastBoard(self, playerturn=None):
        for player in self.playersList:
            if player == playerturn:
                player.send("#" + self.showBoard())
            else:
                player.send(self.showBoard())
            
    def broadCastExclusive(self,player,msg):
        if player == None:
            for p in self.playersList:
                p.send(msg)
        else:
            for p in self.playersList:
                if p != player:
                    p.send(msg)

    def play(self):
        if self.newGame:
            self.setup()
            self.newGame = False
        self.active = True
        while not self.isPuzzleSolved() and not self.isMaxGuesses():
            player = self.nextPlayer()
            if player == None:
                break
            self.broadCastBoard(playerturn=player)
            guess = player.recv()
            correct = self.guess(player,guess)
            while correct and not self.isPuzzleSolved() and not self.isMaxGuesses():
                self.broadCastBoard(playerturn=player)
                guess = player.recv()
                correct = self.guess(player,guess)
                if not correct:
                    break

        if self.isPuzzleSolved():
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
    print("hangman playersList: ", hangman.playersList)
    hangman.play()


