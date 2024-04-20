import hmac
import hashlib
import string
import random
import datetime

acc_number = 3001


class Register:
    def __init__(self):
        self.userInfo = {}
        self.secretKeys = []

    def generateSecretKey(self):
        keysize = 5
        res = "".join(random.choices(string.ascii_uppercase + string.digits, k=keysize))
        return res


class Auth:
    def generate_challenge(self):
        keysize = random.randint(8, 12)
        intchallengemsg = random.getrandbits(keysize)
        return intchallengemsg

    def generate_randomBit(self):
        rbit = random.randint(0, 1)
        return rbit

    def create_response(secret_key, rbit, challenge, amt):
        hash_func = hashlib.sha256
        msg = str(rbit + challenge + amt)
        hmsg = hmac.new(secret_key.encode(), msg.encode(), hash_func)
        hmac_value = hmsg.hexdigest()
        return [amt, hmac_value]

    def verify_response(secret_key, rbit, challenge, hmac_res, amt):
        hash_func = hashlib.sha256
        msg = str(rbit + challenge + amt)
        hmsg = hmac.new(secret_key.encode(), msg.encode(), hash_func)
        hmac_value = hmsg.hexdigest()
        if hmac_value == hmac_res[1] and amt == hmac_res[0]:
            return True
        else:
            return False


reg = Register()
auth = Auth()

print("\t\t******************************************************************")
print("\t\t\t\t\tNET BANKING SYSTEM")
print("\t\t******************************************************************")
print("\t\t\tDeveloped using Blockchain technologies by Group 20")
print("\t\t******************************************************************")
print("\t\t\t\t   Press Enter to open main menu")
input()

while True:
    print(
        """ 
    Select any one of the following : 
        1 : Register User
        2 : Deposit Amount
        3 : Withdraw Amount
        4 : Transfer Amount
        5 : Balance Enquiry
        6 : View Transactions
        7 : All Account holder list
        0 : Exit
    
    """
    )
    choice = input("Enter choice: ")
    if choice == "1":
        uname = input("\nEnter the account holder name : ")
        balance = int(input("Enter The initial deposit amount : "))
        tpin = int(input("Setup pin number (integer format): "))
        print("\n\nAccount Successfully registered!")
        accno = acc_number
        acc_number += 1
        scode = reg.generateSecretKey()
        while scode in reg.secretKeys:
            scode = reg.generateSecretKey()
        print(
            f"Account number: {accno}\nSecret code (never share with others): {scode}\nCurrent Balance: {balance}"
        )
        reg.userInfo[acc_number] = {
            "name": uname,
            "balance": balance,
            "pin": tpin,
            "accountno": accno,
            "secretcode": scode,
        }
        reg.secretKeys.append(scode)
    elif choice == "0":
        break
    elif choice == "2":
        print("\nDEPOSIT AMOUNT")
        login_account = int(input("Enter Account Number: "))
        if login_account in reg.userInfo:
            login_pin = int(input("Enter Pin Number: "))
            if login_pin == reg.userInfo[login_account]:
                deposit_amt = int(input("Enter Deposit Amount: "))
                chal = auth.generate_challenge()
                rbit = auth.generate_randomBit()
                msghmac = auth.create_response(rbit, chal, deposit_amt)
                if auth.verify_response(rbit, chal, msghmac, msghmac[0]):
                    reg.userInfo[login_account]["balance"] += deposit_amt
                    print(
                        # f"Account No. {login_account} credited with {deposit_amt}\nCurrent Balance: f{reg.userInfo[login_account]}\n"
                        f"Account No. {login_account} credited with {deposit_amt}\n"
                    )
                else:
                    print("Authentication failed\n")
            else:
                print("Invalid Pin\n")
        else:
            print("Invalid Account Number\n")

    else:
        print("\nInvalid choice\n\n")
