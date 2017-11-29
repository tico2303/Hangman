#!/usr/bin/python
import random
from users import Player
from os import system
from words import wordlist
import threading

class ThreadedHangman(threading.Thread):
    def __init__(self, name,playersList=[],*args, **kwargs):
        super(ThreadedHangman, self).__init__()
        self.playersList = playersList
        self.hangman = Hangman(name,self.playersList)
        

class Game(object):
#class Game(threading.Thread):
    def __init__(self, name,*args, **kwargs):
        #super(Game, self).__init__()
        self.playersList_lock = threading.Lock()
        self.difficulty = 1
        self.name = name + str(random.randint(0,10000))
        self.active = False

    def add(self,player):
        #self.lock.acquire()
        print("[+] Player: ", player.name, " joined the Game!")
        if player not in self.playersList:
            self.playersList.append(player)
        #self.lock.release()

    def remove(self,player):
        for i, user in enumerate(self.playersList):
            if user.name == player.name:
                del self.playersList[i]
                break
    
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
        self.newGame = True
        self.puzzleCenter = 40
        self.beginSplash = "*******************\n"
        self.bannerSplash = "*" + "HangMan".center(17) + "*\n"
        self.gameNameSplash = "*" + self.name.center(17) + "*\n"
        self.endSplash = "*******************\n\n\n"

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
        #self.lock.acquire()
        self.guesses.append(letter)
        for index,ch in enumerate(self.word):
            if ch == letter and self.puzzle[index] != self.solution[index]: 
                self.puzzle[index] = self.solution[index]
                #print("player", player.name, " got it right")
                player.score +=1 
                #print("his score is: ", player.score)
        #self.lock.release()

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
        #self.lock.acquire()
        print("[+] Getting next player")
        if self.newGame:
            self.turn = 0
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

    def broadCastBoard(self):
        for player in self.playersList:
            player.send(self.showBoard())

    def broadCastExclusive(self,player,msg):
        for p in self.playersList:
            if p != player:
                player.send(msg)

    def play(self):
        if self.newGame:
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
            # keep guessing until you have a wrong answer, puzzle is solved or max guesses is reached
            while correct and not self.isPuzzleSolved() and not self.isMaxGuesses():
                self.broadCastBoard()
                guess = player.recv()
                correct = self.guess(player,guess)
                if not correct:
                    break

        self.active = False
        if self.isPuzzleSolved():
            self.boardCastBoard()
            #player.send(self.showBoard())
            player.send("You Win!\n\n")
            self.broadCastExclusive(player,"You Lose\n\n")
            return self.active 
        else:
            self.boardCastBoard()
            #player.send(self.showBoard())
            self.broadCastExclusive(None, "You Lost\n\n")
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


