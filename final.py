import pickle
import os
import pathlib
import hashlib
import datetime
import random

# Group 11 Members
# Rishav Bhowmick
# Rohan Reddy Amanaganti
# Syed Ameen
# Vivian Pyarry John

class transactionBlock:
    def __init__(self, transactionID, senderID, receiverID, transferAmt, previous_hash):
        self.transactionID = transactionID
        self.senderID = senderID
        self.receiverID = receiverID
        self.transferAmt = transferAmt
        self.previous_hash = previous_hash
        self.timestamp = datetime.datetime.now()
        self.n = 0
        self.hash = self.calculateHash()
  
    def calculateHash(self):
        sha = hashlib.sha256()
        sha.update(str(self.transactionID).encode('utf-8') + 
                   str(self.senderID).encode('utf-8') + 
                   str(self.receiverID).encode('utf-8') + 
                   str(self.transferAmt).encode('utf-8') + 
                   str(self.timestamp).encode('utf-8') + 
                   str(self.previous_hash).encode('utf-8') + 
                   str(self.n).encode('utf-8'))
        return sha.hexdigest()
  
    def mineBlock(self, difficulty):
        while self.hash[0:difficulty] != "0" * difficulty:
            self.n += 1
            self.hash = self.calculateHash()

class transactionBlockchain:
    def __init__(self):
        self.chain = [self.genesisBlock()]

    def genesisBlock(self):
        return transactionBlock("0", "0", "0", "0", "0")
        # Block 0 stores empty values

    def createBlock(self, newBlock, senderID, receiverID, transferAmt):
        previousBlock = self.chain[-1]
        newTransactionID = int(previousBlock.transactionID) + 1
        newBlock.mineBlock(4)
        newBlock = transactionBlock(newTransactionID, senderID, receiverID, transferAmt, previousBlock.hash)  
        self.chain.append(newBlock)

    def printSentTransaction(self, acc):
        print("Sent")
        for block in self.chain:
            if block.senderID == acc:
                print("\tTransaction ID: ", block.transactionID)
                print("\tTransaction Timestamp:", block.timestamp)
                print("\tSender Account No: ", block.senderID)
                print("\tReceiver Account No:", block.receiverID)
                print("\tTransacted Amount: ", block.transferAmt)
                break
        else:
            print("\tNo transaction history available\n")

    def printReceivedTransaction(self, acc):
        print("Received")
        for block in self.chain:
            if block.receiverID == acc:
                print("\tTransaction ID: ", block.transactionID)
                print("\tTransaction Timestamp:", block.timestamp)
                print("\tSender Account No: ", block.receiverID)
                print("\tReceiver Account No:", block.senderID)
                print("\tTransacted Amount: ", block.transferAmt)
                print("\n")
                break
        else:
            print("\tNo transaction history available\n")

class Account :
   accNo = 0
   PassWrd = 0
   name = ''
   balance = 0
   type = ''

   def createAccount(self):
       self.accNo= int(input("Enter the account no (4 digits of ID no.): "))
       self.PassWrd= (input("Enter passcode (integer format): "))
       self.name = input("Enter the account holder name : ")
       self.type = input("Enter the type of account [C/S] : ")
       self.balance = int(input("Enter The initial deposit amount : "))
       print("\n\n\nAccount Created\n\n")

   def showAccount(self):
       print("Account Number : ",self.accNo)
       print("Account Holder Name : ", self.name)
       print("Type of Account", self.type)
       print("Balance : ",self.balance)

   def depositAmount(self,amount):
       self.balance += amount  

   def withdrawAmount(self,amount):
       self.balance -= amount  

   def report(self):
       print(self.accNo, " ",self.name ," ",self.type," ", self.balance)  

   def getAccountNo(self):
       return self.accNo

   def getAcccountHolderName(self):
       return self.name

   def getAccountType(self):
       return self.type

   def getDeposit(self):
       return self.balance

def intro():
   print("\t\t\t**********************")
   print("\t\t\tNET BANKING SYSTEM")
   print("\t\t\t**********************")
   print("\t\t\tDeveloped using Blockchain technologies by Group 11")
   print("\t\t\t**********************")
   print("\t\t\tPress Enter to open main menu")
   input()

def writeAccount():
   account = Account()
   account.createAccount()
   writeAccountsFile(account)

def displayAllAcc():
   file = pathlib.Path("accounts.data")
   if file.exists ():
       infile = open('accounts.data','rb')
       mylist = pickle.load(infile)
       for item in mylist :
           print("Account no: ",item.accNo,"\nAccount Holder name: ", item.name, "\nAccount type: ",item.type,"\n")
       infile.close()
   else :
       print("No records to display")

def displayBal(num, code):
   file = pathlib.Path("accounts.data")
   if file.exists ():
        infile = open('accounts.data','rb')
        mylist = pickle.load(infile)
        infile.close()
        found = False
        for item in mylist :
            if item.accNo == num :
                if item.PassWrd == code:
                    print("Your account Balance is = ",item.balance)
                    found = True
                else :
                    print("Password is incorrect")
                    found = True 
   else :
       print("No records to Search")
   if not found :
       print("No existing record with this account number")

def verifyTransaction(num):
    file = pathlib.Path("accounts.data")
    if file.exists ():
        infile = open('accounts.data','rb')
        mylist = pickle.load(infile)
        infile.close()
        flag = False
        for item in mylist :
            if item.accNo == num :
                p=11  # arbitrary value
                g=2   # arbitrary value
                y=(g**int(item.PassWrd))%p
                r=random.randint(0, p-1)
                h=(g**r)%p
                b=random.randint(0, 1)
                s=(r+b*int(item.PassWrd))%(p-1)
                if ((g**s)%p == h*(y**b)%p):
                    flag = True
                else:
                    flag = False
        if flag:
            return True
        else:
            return False
    else :
        return 1

def depositAndWithdraw(num1, code, num2):
    file = pathlib.Path("accounts.data")
    if file.exists ():
        infile = open('accounts.data','rb')
        mylist = pickle.load(infile)
        infile.close()
        os.remove('accounts.data')
        for item in mylist :
            if item.accNo == num1 :
                if item.PassWrd == code :
                    if num2 == 1 :
                        amount = int(input("Enter the amount to deposit : "))
                        item.balance += amount
                        print("Your account is updated")
                    elif num2 == 2 :
                        amount = int(input("Enter the amount to withdraw : "))
                        if amount <= item.balance :
                            item.balance -=amount
                        else :
                            print("You cannot withdraw larger amount")      
                else :
                    print("Password is incorrect")    
    else :
        print("No records to Search")
    outfile = open('newaccounts.data','wb')
    pickle.dump(mylist, outfile)
    outfile.close()
    os.rename('newaccounts.data', 'accounts.data')  

def updateBal(num1, code, num2, num3):
    file = pathlib.Path("accounts.data")
    if file.exists ():
        infile = open('accounts.data','rb')
        mylist = pickle.load(infile)
        infile.close()
        os.remove('accounts.data')
        flag = False
        for item in mylist :
            if item.accNo == num1:
                if item.PassWrd == code:
                    item.balance -= num3
                else:
                    print("Password is incorrect\n")
                    flag = True
        for item in mylist :        
            if not flag :
                if item.accNo == num2:
                    item.balance += num3
    else :
        print("No records to Search")
    outfile = open('newaccounts.data','wb')
    pickle.dump(mylist, outfile)
    outfile.close()
    os.rename('newaccounts.data', 'accounts.data') 

def writeAccountsFile(account) :  
   file = pathlib.Path("accounts.data")
   if file.exists ():
       infile = open('accounts.data','rb')
       oldlist = pickle.load(infile)
       oldlist.append(account)
       infile.close()
       os.remove('accounts.data')
   else :
       oldlist = [account]
   outfile = open('newaccounts.data','wb')
   pickle.dump(oldlist, outfile)
   outfile.close()
   os.rename('newaccounts.data', 'accounts.data')      

# start of the program

ch=''
num=0
sender=0
receiver=0
password=''

blockchain = transactionBlockchain()

intro()
while ch != 8:
   #system("cls");
   print("\tMAIN MENU")
   print("\t1. NEW ACCOUNT")
   print("\t2. DEPOSIT AMOUNT")
   print("\t3. WITHDRAW AMOUNT")  
   print("\t4. BALANCE ENQUIRY")
   print("\t5. TRANSFER AMOUNT") 
   print("\t6. ALL ACCOUNT HOLDER LIST")
   print("\t7. VIEW ALL TRANSACTIONS")
   print("\t8. EXIT")
   ch = input("\tSelect Your Option (1-8) : ")
   #system("cls");  
   if ch == '1':
       writeAccount()
   elif ch =='2':
       num = int(input("\tEnter Your account No. : "))
       password = input("\tEnter Your Password : ")
       depositAndWithdraw(num, password, 1)
   elif ch == '3':
       num = int(input("\tEnter Your account No. : "))
       password = input("\tEnter Your Password : ")
       depositAndWithdraw(num, password, 2)
   elif ch == '4':
       num = int(input("\tEnter Your account No. : "))
       password = input("\tEnter Your Password : ")
       displayBal(num, password)
   elif ch == '5':
       sender = int(input("\tEnter Your account No. : "))
       password = input("\tEnter Your Password : ")
       receiver = int(input("\tEnter The Receiver's account No. : "))
       amount = int(input("\tEnter amount to be transferred : "))
       updateBal(sender, password, receiver, amount)
       block = transactionBlock("", sender, receiver, amount, "")
       blockchain.createBlock(block, sender, receiver, amount)
   elif ch == '6':
       displayAllAcc()
   elif ch == '7':
        num =int(input("\tEnter Your account No. : "))
        password = input("\tEnter Your Password : ")
        if verifyTransaction(num) == True:
            blockchain.printSentTransaction(num)
            blockchain.printReceivedTransaction(num)
        elif verifyTransaction == 1 :
            print("No account exists under this ID")
        else :
            print("Password is incorrect\n")      
   elif ch == '8':
       print("\tThank you for using our Net Banking System!")
       break
   else :
       print("Invalid choice")  
       ch = input("Enter your choice : ")  