import pickle

class Repo(object):
    def __init__(self,filename):
        self.filename = filename

    def getData(self):
        try:
            return pickle.load(open(self.filename,'rb')) 
        except EOFError:
            return []

    def saveData(self,data):
        pickle.dump(data,open(self.filename, 'wb'))

class HallofFameRepo(Repo):
    def __init__(self,filename):
        super(HallofFameRepo,self).__init__(filename)

class UsersRepo(Repo):
    def __init__(self,filename):
        super(UsersRepo,self).__init__(filename)
    
class WordRepo(Repo):
    def __init__(self,filename):
        super(WordRepo,self).__init__(filename)

if __name__ == "__main__":
    hof = [('Robert',3), ('otherguy',10)]
    filename = "halloffameDB.pkl"
    h = HallofFameRepo(filename)
    h.saveData(hof)
    print h.getData() 
    
