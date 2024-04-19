import hmac
import hashlib

print("\t\t******************************************************************")
print("\t\t\t\t\tNET BANKING SYSTEM")
print("\t\t******************************************************************")
print("\t\t\tDeveloped using Blockchain technologies by Group 20")
print("\t\t******************************************************************")
print("\t\t\t\t   Press Enter to open main menu")
input()


class Register:
    def __init__(self):
        self.userInfo = {}


secret_key = b"your_secret_key_here"
message = "This is a secret message!"

hash_function = hashlib.sha256

h = hmac.new(secret_key, message.encode(), hash_function)
hmac_value = h.hexdigest()

print(f"HMAC value: {hmac_value}")

received_message = "This is a secret message!"  # Can be tampered with for testing
received_hmac_value = "abad58a1ca2f266bde0002fde8719cd2478f8a2995f58e25352cf176f15993fa"

# Generate HMAC for verification
h_verify = hmac.new(secret_key, received_message.encode(), hash_function)
verification_hmac = h_verify.hexdigest()

# Check if received HMAC matches generated HMAC
if verification_hmac == received_hmac_value:
    print("Message is authentic!")
else:
    print("Message has been tampered with!")
# while True:
#     # system("cls");
#     print("\tMAIN MENU")
#     print("\t1. NEW ACCOUNT")
#     print("\t2. DEPOSIT AMOUNT")
#     print("\t3. WITHDRAW AMOUNT")
#     print("\t4. BALANCE ENQUIRY")
#     print("\t5. TRANSFER AMOUNT")
import hmac
import hashlib
import string
import random

class Register:
    def __init__(self):
        self.userInfo={}
        self.secretKey=[]
        
    def generateSecretKey():
        keysize=5
        res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=keysize))
        print("The generated random string : " + str(res))
while True:
    print(
       """ 
    Select any one of the following : 
        1 : Register
        2 : Add block onto blockchain 
        3 : View blockchain / transactions
        4 : Buy a product (Client Request) 
        5 : Deliver item (dist -> client)
        6 : View Product Status (QR Code)
        7 : View Pending orders
        8 : Resolve Conflict (Client/Distributor Complaining about delivery of products)  
        9 : View profile
        0 : Exit
    
    """
    )
    choice= input('Enter choice')
    if choice=='1':
        uname= input("Enter your name: ")
        
    else:
        print('error')
#     print("\t6. ALL ACCOUNT HOLDER LIST")
#     print("\t7. VIEW ALL TRANSACTIONS")
#     print("\t8. EXIT")
#     ch = input("\tSelect Your Option (1-8) : ")
#     # system("cls");
#     if ch == "1":
#         createAccount()
#     elif ch == "2":
#         num = int(input("\tEnter Your account No. : "))
#         password = input("\tEnter Your Password : ")
#         depositAndWithdraw(num, password, 1)
#     elif ch == "3":
#         num = int(input("\tEnter Your account No. : "))
#         password = input("\tEnter Your Password : ")
#         depositAndWithdraw(num, password, 2)
#     elif ch == "4":
#         num = int(input("\tEnter Your account No. : "))
#         password = input("\tEnter Your Password : ")
#         displayBal(num, password)
#     elif ch == "5":
#         sender = int(input("\tEnter Your account No. : "))
#         password = input("\tEnter Your Password : ")
#         receiver = int(input("\tEnter The Receiver's account No. : "))
#         amount = int(input("\tEnter amount to be transferred : "))
#         updateBal(sender, password, receiver, amount)
#         block = transactionBlock("", sender, receiver, amount, "")
#         blockchain.createBlock(block, sender, receiver, amount)
#     elif ch == "6":
#         displayAllAcc()
#     elif ch == "7":
#         num = int(input("\tEnter Your account No. : "))
#         password = input("\tEnter Your Password : ")
#         if verifyTransaction(num) == True:
#             blockchain.printSentTransaction(num)
#             blockchain.printReceivedTransaction(num)
#         elif verifyTransaction == 1:
#             print("No account exists under this ID")
#         else:
#             print("Password is incorrect\n")
#     elif ch == "8":
#         print("\tThank you for using our Net Banking System!")
#         break
#     else:
#         print("Invalid choice")
#         ch = input("Enter your choice : ")

# import hmac
# import hashlib
# import string
# import random

# class Register:
#     def __init__(self):
#         self.userInfo={}
#         self.secretKey=[]
        
#     def generateSecretKey():
#         keysize=5
#         res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=keysize))
#         print("The generated random string : " + str(res))
# while True:
#     print(
#        """ 
#     Select any one of the following : 
#         1 : Register
#         2 : Add block onto blockchain 
#         3 : View blockchain / transactions
#         4 : Buy a product (Client Request) 
#         5 : Deliver item (dist -> client)
#         6 : View Product Status (QR Code)
#         7 : View Pending orders
#         8 : Resolve Conflict (Client/Distributor Complaining about delivery of products)  
#         9 : View profile
#         0 : Exit
    
#     """
#     )
#     choice= input('Enter choice')
#     if choice=='1':
#         uname= input("Enter your name: ")
        
#     else:
#         print('error')
