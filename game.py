#!/usr/bin/python
import random
from users import Player
from os import system
from words import wordlist

class Game(object):
    def __init__(self,name=None):
        self.playersList = []
        self.difficulty = 1
        self.name = name + str(random.randint(0,10000))
        self.active = False

    def add(self,player):
        self.playersList.append(player)

    def remove(self,player):
        for i, user in enumerate(self.playersList):
            if user.name == player.name:
                del self.playersList[i]
                break
    
    def play(self):
        raise NotImplementedError

class Hangman(Game):
    def __init__(self,name=None):
        super(Hangman,self).__init__(name) 
        self.wordList = wordlist    
        self.solution = {}
        self.playersList = []
        self.guesses = []
        self.word = None
        self.turn = 0
        self.puzzleCenter = 40
        self.beginSplash = "*******************\n"
        self.bannerSplash = "*" + "HangMan".center(17) + "*\n"
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
        self.guesses.append(letter)
        for index,ch in enumerate(self.word):
            if ch == letter and self.puzzle[index] != self.solution[index]: 
                self.puzzle[index] = self.solution[index]
                #print("player", player.name, " got it right")
                player.score +=1 
                #print("his score is: ", player.score)

    def guessWord(self, player, word):
        if word.lower() == self.word.lower():
            player.score += len(self.word)
            self.puzzle = self.word
            return True
        else:
            return False

    def setup(self):
        print("[+] Setting up hangman game")
        self.word = self.getRandomWord()
        self.puzzle = [ "_" for i in range(len(self.word))]
        for index, letter in enumerate(self.word):
            self.solution[index] = letter

    def nextPlayer(self):
        print("[+] Getting next player")
        print("turn: ", self.turn)
        self.turn += 1 
        self.turn = self.turn %(len(self.playersList))
        player = self.playersList[self.turn]         
        return player

    def showPuzzle(self):
        print("[+] Showing Puzzle")
        return " ".join(self.puzzle).center(self.puzzleCenter) + "\n\n"

    def showPlayers(self):
        print("[+] Showing players")
        display = []
        for i, player in enumerate(self.playersList):
            if i == self.turn:
                display.append(player.name +": "+str(player.score)+ " *\n")
            else:
                display.append(player.name +": "+str(player.score)+ "\n")
        return " ".join(display)+"\n"

    def showGuesses(self):
        print("[+] Showing Guesses")
        return " ".join(self.guesses) + "\n\n\n"

    def showBoard(self):
        print("[+] Showing Board to: ", self.playersList[self.turn].name)        
        banner = self.beginSplash + self.bannerSplash + self.endSplash
        board = banner + self.showPuzzle() +  self.showGuesses()+ self.showPlayers() 
        return board

    def play(self):
        self.setup()             
        self.active = True
        print("[+] Starting Game loop")
        while not self.isPuzzleSolved() and not self.isMaxGuesses():
            
            player = self.nextPlayer() 
            player.send(self.showBoard())
            #guess = raw_input("guess a letter: ") 
            guess = player.conn.recv(1024)
            if len(guess) <= 1:
                self.guessLetter(player, guess)
            else:
                correct = self.guessWord(player,guess)
                break

        if self.isPuzzleSolved():
            player.send(self.showBoard())
            player.send("You Won!\n\n")
            self.active = False
        else:
            player.send(self.showBoard())
            player.send("You Lost!\n\n")
    
            
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


