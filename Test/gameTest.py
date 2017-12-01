#!/usr/bin/python
import random
from users import Player
from os import system
from words import wordlist
import threading

#class Game(threading.Thread):
class Game(object):
    def __init__(self, name,*args, **kwargs):
        #super(Game, self).__init__()
        #self.lock = threading.Lock()
        self.difficulty = 1
        self.name = name + str(random.randint(0,10000))
        self.active = False
        self.end = False

    def add(self,player):
        #self.lock.acquire()
        print("[+] Player: ", player, " joined the Game!")
        if player not in self.playersList:
            self.playersList.append(player)
        #self.lock.release()

    def remove(self,player):
        print("removing player")
        if len(self.playersList) > 0:
            for i, user in enumerate(self.playersList):
                if user.name == player.name:
                    del self.playersList[i]
                    break
        else:
            print("No more players setting end")
            self.end = True

    
    def play(self):
        raise NotImplementedError

class Hangman(Game):
    def __init__(self,name=None, playersList=[], *args, **kwargs):
        super(Hangman,self).__init__(name,*args, **kwargs) 
        self.wordList = wordlist    
        self.playersList = playersList
        self.solution = {}
        self.guesses = []
        self.word = None
        self.turn = 0
        self.puzzleCenter = 40
        self.beginSplash = "*******************\n"
        self.bannerSplash = "*" + "HangMan".center(17) + "*\n"
        self.endSplash = "*******************\n\n\n"
        self.newGame = True

    def addWord(self,word):
        if word not in self.wordList:
            self.wordList.append(word)        


    def getRandomWord(self):
        return random.choice(self.wordList)         

    def isPuzzleSolved(self):
        if "_" not in self.puzzle or self.end:
            return True
        else:
            return False

    def isMaxGuesses(self):
        if len(self.guesses) >= (len(self.word) * (4-int(self.difficulty))):
            return True
        else:   
            return False

    def guessLetter(self, player, letter):
        #print("[+] Guessing letter")
        #self.lock.acquire()
        self.guesses.append(letter)
        for index,ch in enumerate(self.word):
            if ch == letter and self.puzzle[index] != self.solution[index]: 
                self.puzzle[index] = self.solution[index]
                print("player", player.name, " got it right")
                player.score +=1 
                return True
                #print("his score is: ", player.score)
        return False
        #self.lock.release()

    def guessWord(self, player, word):
        print("Guessing word!")
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
                print("Incorrect word guess.. removing player")
                self.remove(player)
        return correct
        
        
    def setup(self):
        print("[+] Setting up hangman game")
        self.word = self.getRandomWord()
        self.puzzle = [ "_" for i in range(len(self.word))]
        for index, letter in enumerate(self.word):
            self.solution[index] = letter

    def nextPlayer(self):
        #self.lock.acquire()
        print("[+] Getting next player")
        if self.newGame:
            self.turn = 0
            self.newGame = False
        else:
            self.turn += 1 
        print("turn index: ", self.turn%(len(self.playersList)))
        self.turn = self.turn %(len(self.playersList))
        player = self.playersList[self.turn]         
        print("player at turn index: ", player.name)
        print("playersList: ", [p.name for p in self.playersList])
        #self.lock.release()
        return player

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
        return "Guesses: "+ " ".join(self.guesses) + "\n\n\n"

    def showBoard(self):
        #print("[+] Showing Board to: ", self.playersList[self.turn%(len(self.playersList))])        
        banner = self.beginSplash + self.bannerSplash + self.endSplash
        board = banner + self.showPuzzle() +  self.showGuesses()+ self.showPlayers() 
        return board

    def broadCastBoardAll(self):
        for player in self.playersList:
            #if player != self.playersList[self.turn%(len(self.playersList))]:
            player.send(self.showBoard())

    def broadCastBoard(self,player):
        for p in self.playersList:
            if p != player:
                player.send(self.showBoard())

    def play(self):
        self.setup()             
        self.active = True
        print("[+] Starting Game loop")
        pl = [Player(name="NewGuy1"),Player(name="AnotherPlayer1")] 
        count = 0
        while not self.isPuzzleSolved() or not self.isMaxGuesses():
            player = self.nextPlayer() 
            self.broadCastBoardAll()
            guess = player.recv()
            correct = self.guess(player,guess)
            if count <2:
                self.add(pl[count])
            count +=1
            
            while correct and not self.isPuzzleSolved() and not self.isMaxGuesses():
                self.broadCastBoardAll()
                guess = player.recv()
                correct = self.guess(player,guess)
                if not correct:
                    break
                 

        self.active = False
        if self.isPuzzleSolved():
            self.broadCastBoardAll()
            #player.send(self.showBoard())
            player.send("You Won!\n\n")
            for p in self.playersList:
                if p != player:
                    p.send("You Lose\n")
            return self.active 
        else:
            self.broadCastBoardAll()
            #player.send(self.showBoard())
            player.send("You Lost!\n\n")
            return self.active
    
            
if __name__ == "__main__":
    from users import Player

    hangman = Hangman(name="TestGame")
    hangman.difficulty = 2
    playerList = []  
    for player in ["Tom", "Dick"]:
        p = Player(name=player) 
        playerList.append(p) 
        hangman.add(p)     
    hangman.play()
    #hangman.playersList = playerList
    print("hangman playersList: ", hangman.playersList)


