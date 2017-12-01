import threading
import time
import random

class BankAccount(threading.Thread):
    # static var of the class
    # value persists through different instances and 
    # changes in one instance effect state of the var in other instances 
    accntBalance = 100    

    def __init__(self, name, moneyRequest):
        threading.Thread.__init__(self)

        self.name = name
        self.moneyRequest = moneyRequest

    def run(self):
        threadLock.acquire()
        BankAccount.getMoney(self)

        threadLock.release()

    @staticmethod
    def getMoney(Bankcustomer):
        print("{} tries to withdrawl ${} at time: {}".format(Bankcustomer.name,Bankcustomer.moneyRequest,time.strftime("%H:%M:%S",time.gmtime())))

        if BankAccount.accntBalance - Bankcustomer.moneyRequest > 0:
            BankAccount.accntBalance -= Bankcustomer.moneyRequest
            print("New Bank Account balance: {}\n".format(BankAccount.accntBalance))
        else:
            print("Not enough money in bank")
            print("Current balance: {}\n".format(BankAccount.accntBalance))
        time.sleep(1)

#threadLock must be global to the class instance
threadLock = threading.Lock()

# assumes all users share the same resource accntBalance
bill = BankAccount("bill", 20)
nye = BankAccount("nye", 10)
scigy = BankAccount("scienceGuy", 50)
sherry = BankAccount("sherry", 80)

#starts the threads
bill.start()
nye.start()
scigy.start()
sherry.start()

#kills the threads after there don
bill.join()
nye.join()
scigy.join()
sherry.join()

