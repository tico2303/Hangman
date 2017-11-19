import random
from users import Player

class Game(object):
    def __init__(self):
        self.playersList = []
        self.difficulty = 1

    def join(self,player):
        self.playersList.append(player)

    def leave(self,player):
        for i, user in enumerate(self.playersList):
            if user.name == player.name:
                del self.playersList[i]
                break

    def play(self):
        raise NotImplementedError

class Hangman(Game):
    def __init__(self):
        super(Hangman,self).__init__() 
        self.wordList = ["hangman", "netties", "cool"]      
        self.solution = {}
        self.playersList = []
        self.guesses = []
        self.word = None
        self.turn = 0

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
        self.guesses.append(letter)
        for index,ch in enumerate(self.word):
            if ch == letter and self.puzzle[index] != self.solution[index]: 
                self.puzzle[index] = self.solution[index]
                print("player", player.name, " got it right")
                player.score +=1 
                print("his score is: ", player.score)

    def guessWord(self, player, word):
        if word.lower() == self.word.lower():
            player.score += len(self.word)
            print("You WIN")
            return True
        else:
            print("You lose")
            return False

    def setup(self):
        self.word = self.getRandomWord()
        self.puzzle = [ "_" for i in range(len(self.word))]
        for index, letter in enumerate(self.word):
            self.solution[index] = letter

    def nextPlayer(self):
        print("turn: ", self.turn)
        self.turn += 1 
        self.turn = self.turn %(len(self.playersList))
        player = self.playersList[self.turn]         
        return player

    def showPuzzle(self):
        return " ".join(self.puzzle).center(40) + "\n"

    def showPlayers(self):
        display = []
        for i, player in enumerate(self.playersList):
            if i == self.turn:
                display.append(player.name +": "+str(player.score)+ " *\n")
            else:
                display.append(player.name +": "+str(player.score)+ "\n")
        return " ".join(display)

    def showGuesses(self):
        return " ".join(self.guesses) + "\n\n\n"

    def showBoard(self):
        return self.showPuzzle() +  self.showGuesses()+ self.showPlayers() 

    def play(self):
        self.setup()             
        while not self.isPuzzleSolved() and not self.isMaxGuesses():
            player = self.nextPlayer() 
            player.conn.send(self.showBoard())
            #guess = raw_input("guess a letter: ") 
            guess = player.conn.recv(1024)
            self.guessLetter(player, guess)

        if self.isPuzzleSolved():
            self.showBoard()
            


if __name__ == "__main__":

    playerList = []  
    for player in ["Tom", "Dick"]:
       playerList.append(Player(player, "connection")) 
    hangman = Hangman()
    hangman.playersList = playerList
    print(hangman.playersList)
    hangman.join(Player("Timmy","connection"))
    hangman.play()



