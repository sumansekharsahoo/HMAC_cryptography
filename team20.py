import hmac
import hashlib
import string
import random
import time

acc_number = 3001
trans_id = 5001


class Account:
    def __init__(self):
        self.userInfo = {}
        self.secretKeys = []
        self.transactions = {}

    def generateSecretKey(self):
        keysize = 5
        res = "".join(random.choices(string.ascii_uppercase, k=keysize))
        return res

    def viewUser(self, accno):
        print(f"Transactions done by Account No. {accno}:\n")
        for i in self.transactions[accno]:
            if i[1] == "D":
                print(f"{i[0]}: Deposited amount: {i[2]}")
            elif i[1] == "W":
                print(f"{i[0]}: Widrawal amount: {i[2]}")
            elif i[1] == "Tin":
                print(
                    f"{i[0]}: Transfered from (credited) AccountNo. {i[2]} amount {i[3]}"
                )
            elif i[1] == "Tout":
                print(
                    f"{i[0]}: Transfered to (debited) AccountNo. {i[2]} amount {i[3]}"
                )


class Auth:
    def generate_challenge(self):
        keysize = random.randint(8, 12)
        intchallengemsg = random.getrandbits(keysize)
        return intchallengemsg

    def generate_randomBit(self):
        rbit = random.randint(0, 1)
        return rbit

    def create_response(self, secret_key, rbit, challenge, amt):
        hash_func = hashlib.sha256
        msg = str(rbit + challenge + amt)
        hmsg = hmac.new(secret_key.encode(), msg.encode(), hash_func)
        hmac_value = hmsg.hexdigest()
        return [amt, hmac_value]

    def verify_response(self, secret_key, rbit, challenge, hmac_res, amt):
        hash_func = hashlib.sha256
        msg = str(rbit + challenge + amt)
        hmsg = hmac.new(secret_key.encode(), msg.encode(), hash_func)
        hmac_value = hmsg.hexdigest()
        if hmac_value == hmac_res[1] and amt == hmac_res[0]:
            return [True, hmac_value]
        else:
            return [False, hmac_value]


class Blockchain:
    def __init__(self):
        self.verifiedTransac = {}
        self.pendingTranac = {}
        self.blockchainedTransac = {}
        self.chain = []
        self.blockNotMined = []

    def initiategenesisblock(self, timestmp):
        blk = {
            "index": len(self.chain) + 1,
            "merkleroot": "0",
            "trans_ID": "0",
            "timestamp": timestmp,
            "blockproducer": "0",
            "blockminer": "0",
            "prevhash": "0",
            "hash": "0",
        }
        self.chain.append(blk)
        blk_msg = f"""
[
    index: {blk['index']},
    merkleroot: {blk['merkleroot']},
    transaction_IDs: nil,
    timestamp: {blk['timestamp']},
    blockproducer: 0
    blockminer: 0
    prevhash: {blk['prevhash']},
    hash: {blk['hash']}
]
"""
        print("Genesis Block:\n")
        print(blk_msg)

    def addUnverifiedTransaction(self, timestamp, transaction, tid):
        msg = f"""[
            transaction_id: {tid}
            timestamp: {timestamp},
            transaction: {transaction}
]"""
        self.pendingTranac[tid] = msg
        return msg

    def verifytransaction(self, transac_id, accno, skey, auth, acc):
        chal = auth.generate_challenge()
        print(f"\nRandom challenge: {chal}")
        rbit = auth.generate_randomBit()
        print(f"Random bit: {rbit}")
        msghmac = auth.create_response(skey, rbit, chal, transac_id)
        print(f"Response HMAC digest: {msghmac[1]}")
        verif = auth.verify_response(
            acc.userInfo[accno]["secretkey"],
            rbit,
            chal,
            msghmac,
            msghmac[0],
        )
        print(f"Calculated HMAC digest: {verif[1]}")
        if verif[0]:
            print("Calculated HMAC matched with received response!")
            self.verifiedTransac[transac_id] = self.pendingTranac[transac_id]
            del self.pendingTranac[transac_id]
            print(f"\nTransactionID: {transac_id} is verified!\n")
        else:
            print("Calculated HMAC did not match with received response")
            print("Authentication failed\n")

    def merkletree(self, t1, t2, t3):
        hashed = []
        t1_msg = self.verifiedTransac[t1]
        t2_msg = self.verifiedTransac[t2]
        t3_msg = self.verifiedTransac[t3]
        hashed.append(str(hashlib.sha256(t1_msg.encode()).hexdigest()))
        hashed.append(str(hashlib.sha256(t2_msg.encode()).hexdigest()))
        hashed.append(str(hashlib.sha256(t3_msg.encode()).hexdigest()))
        hash12_msg = hashed[0] + hashed[1]
        hash12 = str(hashlib.sha256(hash12_msg.encode()).hexdigest())
        hash33_msg = hashed[2] + hashed[2]
        hash33 = str(hashlib.sha256(hash33_msg.encode()).hexdigest())
        hash1233_msg = hash12 + hash33
        hash1233 = str(hashlib.sha256(hash1233_msg.encode()).hexdigest())
        return hash1233

    def createBlock(self, blkproducer):
        blk_dict = {}
        blk_dict["index"] = len(self.chain) + 1
        tids = []
        ct = 0
        for i in self.verifiedTransac:
            if ct >= 3:
                break
            else:
                ct += 1
                tids.append(i)
        tidstr = ""
        for i in tids:
            tidstr += str(i)
            tidstr += " "
        blk_dict["trans_ID"] = tidstr
        merkleroothash = self.merkletree(tids[0], tids[1], tids[2])
        blk_dict["merkleroot"] = merkleroothash
        blk_dict["blockproducer"] = str(blkproducer)
        self.blockNotMined.append(blk_dict)
        for j in tids:
            self.blockchainedTransac[j] = self.verifiedTransac[j]
            del self.verifiedTransac[j]
        print("\nBlock created!\n")
        ind = self.blockNotMined[len(self.blockNotMined) - 1]["index"]
        mkrt = self.blockNotMined[len(self.blockNotMined) - 1]["merkleroot"]
        tidsbnm = self.blockNotMined[len(self.blockNotMined) - 1]["trans_ID"]
        bp = self.blockNotMined[len(self.blockNotMined) - 1]["blockproducer"]
        blkmsg = f"""[
        index: {ind}
        merkleroot: {mkrt}
        transaction_IDs: {tidsbnm}
        blockproducer: {bp}
]"""
        return blkmsg

    def printBlock(self, blk_dict):
        ind = blk_dict["index"]
        mkrt = blk_dict["merkleroot"]
        tidsbnm = blk_dict["trans_ID"]
        bp = blk_dict["blockproducer"]
        phash = blk_dict["prevhash"]
        hhash = blk_dict["hash"]
        tstamp = blk_dict["timestamp"]
        blkminer = blk_dict["blockminer"]
        blkmsg = f"""[
        index: {ind},
        merkleroot: {mkrt},
        transaction_IDs: {tidsbnm},
        timestamp: {tstamp},
        blockproducer: {bp},
        blockminer: {blkminer},
        prevhash: {phash},
        hash: {hhash}
]
"""
        return blkmsg

    def mineBlock(self, blkminer, tstamp):
        blk_dict = self.blockNotMined.pop(0)
        blk_dict["prevhash"] = self.chain[len(self.chain) - 1]["hash"]
        blk_dict["timestamp"] = tstamp
        blk_dict["blockminer"] = blkminer
        strforhash = blk_dict["prevhash"] + str(tstamp) + str(blkminer)
        blk_dict["hash"] = str(hashlib.sha256(strforhash.encode()).hexdigest())
        self.chain.append(blk_dict)
        return self.printBlock(blk_dict)


acc = Account()
auth = Auth()
blk = Blockchain()

blk.initiategenesisblock(time.time())

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
        5 : Verify Transaction(s)
        6 : Create / Mine Block
        7 : View Blockchain / Transactions
        8 : View User Transactions
        9 : View User Details 
        0 : Exit
    
    """
    )
    choice = input("Enter choice: ")
    if choice == "1":
        uname = input("\nEnter the account holder name : ")
        balance = int(input("Enter The initial deposit amount : "))
        # tpin = int(input("Setup pin number (integer format): "))
        print("\n\nAccount Successfully registered!")
        accno = acc_number
        acc_number += 1
        scode = acc.generateSecretKey()
        while scode in acc.secretKeys:
            scode = acc.generateSecretKey()
        print(
            f"Account number: {accno}\nSecret key (never share with others): {scode}\nCurrent Balance: {balance}"
        )
        acc.userInfo[accno] = {
            "name": uname,
            "balance": balance,
            "accountno": accno,
            "secretkey": scode,
        }
        acc.transactions[accno] = []
        acc.secretKeys.append(scode)

    elif choice == "0":
        break
    elif choice == "2":
        print("\nDEPOSIT AMOUNT")
        login_account = int(input("Enter Account Number: "))
        if login_account in acc.userInfo:
            deposit_amt = int(input("Enter Deposit Amount: "))
            skey = input("Enter secret key: ")
            chal = auth.generate_challenge()
            print(f"\nRandom challenge: {chal}")
            rbit = auth.generate_randomBit()
            print(f"Random bit: {rbit}")
            msghmac = auth.create_response(skey, rbit, chal, deposit_amt)
            print(f"Response HMAC digest: {msghmac[1]}")
            verif = auth.verify_response(
                acc.userInfo[login_account]["secretkey"],
                rbit,
                chal,
                msghmac,
                msghmac[0],
            )
            print(f"Calculated HMAC digest: {verif[1]}")
            if verif[0]:
                print("Calculated HMAC matched with received response!")
                acc.userInfo[login_account]["balance"] += deposit_amt
                acc.transactions[login_account].append([trans_id, "D", deposit_amt])
                trans_mempool = blk.addUnverifiedTransaction(
                    time.time(),
                    f"AccountNo. {login_account} Deposited amount {deposit_amt}",
                    trans_id,
                )
                trans_id += 1
                print(
                    f"\nAccount No. {login_account} credited with {deposit_amt}\nCurrent Balance: {acc.userInfo[login_account]['balance']}\n"
                )
                print("\nTransaction added to Mempool: ")
                print(trans_mempool)
            else:
                print("Calculated HMAC did not match with received response")
                print("Authentication failed\n")
        else:
            print("Invalid Account Number\n")

    elif choice == "3":
        print("\nWITHDRAW AMOUNT")
        login_account = int(input("Enter Account Number: "))
        if login_account in acc.userInfo:
            wd_amt = int(input("Enter Withdrawal amount: "))
            if acc.userInfo[login_account]["balance"] > wd_amt:
                skey = input("Enter secret key: ")
                chal = auth.generate_challenge()
                print(f"\nRandom challenge: {chal}")
                rbit = auth.generate_randomBit()
                print(f"Random bit: {rbit}")
                msghmac = auth.create_response(skey, rbit, chal, wd_amt)
                print(f"Response HMAC digest: {msghmac[1]}")
                verif = auth.verify_response(
                    acc.userInfo[login_account]["secretkey"],
                    rbit,
                    chal,
                    msghmac,
                    msghmac[0],
                )
                print(f"Calculated HMAC digest: {verif[1]}")
                if verif[0]:
                    print("Calculated HMAC matched with received response!")
                    acc.userInfo[login_account]["balance"] -= wd_amt
                    acc.transactions[login_account].append([trans_id, "W", wd_amt])
                    trans_mempool = blk.addUnverifiedTransaction(
                        time.time(),
                        f"AccountNo. {login_account} Withdrawal amount {wd_amt}",
                        trans_id,
                    )
                    trans_id += 1
                    print(
                        f"\nAccount No. {login_account} debited with {wd_amt}\nCurrent Balance: {acc.userInfo[login_account]['balance']}\n"
                    )
                    print("\nTransaction added to Mempool: ")
                    print(trans_mempool)
                else:
                    print("Calculated HMAC did not match with received response")
                    print("Authentication failed\n")
            else:
                print("Insufficient Balance\n")
        else:
            print("Invalid Account Number\n")
    elif choice == "4":
        print("\nTRANSFER AMOUNT")
        from_acc = int(input("Enter Source Account Number: "))
        if from_acc in acc.userInfo:
            to_acc = int(input("Enter Destination Account Number: "))
            if to_acc in acc.userInfo:
                tranf_amt = int(input("Enter amount to be transfered: "))
                if acc.userInfo[from_acc]["balance"] > tranf_amt:
                    skey = input("Enter Secret Key: ")
                    chal = auth.generate_challenge()
                    print(f"\nRandom challenge: {chal}")
                    rbit = auth.generate_randomBit()
                    print(f"Random bit: {rbit}")
                    msghmac = auth.create_response(skey, rbit, chal, tranf_amt)
                    print(f"Response HMAC digest: {msghmac[1]}")
                    verif = auth.verify_response(
                        acc.userInfo[from_acc]["secretkey"],
                        rbit,
                        chal,
                        msghmac,
                        msghmac[0],
                    )
                    print(f"Calculated HMAC digest: {verif[1]}")
                    if verif[0]:
                        print("Calculated HMAC matched with received response!")
                        acc.userInfo[from_acc]["balance"] -= tranf_amt
                        acc.userInfo[to_acc]["balance"] += tranf_amt
                        acc.transactions[from_acc].append(
                            [trans_id, "Tout", to_acc, tranf_amt]
                        )
                        acc.transactions[to_acc].append(
                            [trans_id, "Tin", from_acc, tranf_amt]
                        )
                        trans_mempool = blk.addUnverifiedTransaction(
                            time.time(),
                            f"AccountNo. {from_acc} transfered to AccountNo. {to_acc} amount {tranf_amt}",
                            trans_id,
                        )
                        trans_id += 1
                        print(
                            f"\nAccount No. {from_acc} debited with {tranf_amt}\nCurrent Balance: {acc.userInfo[login_account]['balance']}\n"
                        )
                        print("\nTransaction added to Mempool: ")
                        print(trans_mempool)
                    else:
                        print("Calculated HMAC did not match with received response")
                        print("Authentication failed\n")
                else:
                    print("Insufficient Balance\n")
            else:
                print("Account not found\n")
        else:
            print("Invalid Account Number\n")
    elif choice == "5":
        print("VERIFY TRANSACTION(S)")
        login_account = int(input("Enter Account Number: "))
        if login_account in acc.userInfo:
            ch = input(
                "1: Verify a Transaction\n2: Verify all Transactions\nSelect Action: "
            )
            if ch == "1":
                print("Unverified Transaction ID List: ")
                for i in blk.pendingTranac:
                    print(i)
                transac_id = int(input("Enter Transaction ID: "))
                if i in blk.pendingTranac:
                    skey = input("Enter your secret key: ")
                    blk.verifytransaction(transac_id, login_account, skey, auth, acc)
                else:
                    print("Invalid TransactionID\n")
            elif ch == "2":
                print("Unverified TransactionID list: ")
                unverif_transacID = []
                for i in blk.pendingTranac:
                    print(i)
                    unverif_transacID.append(i)
                skey = input("Enter your secret key: ")
                for i in unverif_transacID:
                    blk.verifytransaction(i, login_account, skey, auth, acc)
            else:
                print("Invalid action\n")
        else:
            print("Invalid Account Number\n")
    elif choice == "6":
        print("\nCREATE/MINE BLOCK")
        if len(blk.verifiedTransac) + len(blk.blockchainedTransac) < 3:
            print("\nMinimum of 3 transactions needed to create/mine a block\n")
        else:
            ch = input("\n1: Create Block\n2: Mine Block\nSelect Action: ")
            if ch == "1":
                if len(blk.verifiedTransac) < 3:
                    print("\nMinimum of 3 transactions needed to create a block\n")
                else:
                    login_account = random.randint(3001, acc_number - 1)
                    print(f"\nAccountNo {login_account} is creating a block\n")
                    skey = acc.userInfo[login_account]["secretkey"]
                    chal = auth.generate_challenge()
                    print(f"\nRandom challenge: {chal}")
                    rbit = auth.generate_randomBit()
                    print(f"Random bit: {rbit}")
                    msghmac = auth.create_response(skey, rbit, chal, login_account)
                    print(f"Response HMAC digest: {msghmac[1]}")
                    verif = auth.verify_response(
                        acc.userInfo[login_account]["secretkey"],
                        rbit,
                        chal,
                        msghmac,
                        msghmac[0],
                    )
                    print(f"Calculated HMAC digest: {verif[1]}")
                    if verif[0]:
                        print("Calculated HMAC matched with received response!")
                        blkmsg = blk.createBlock(login_account)
                        print(blkmsg)
                    else:
                        print("pasjndf allabsd msidilasdb")
            elif ch == "2":
                if len(blk.blockNotMined) == 0:
                    print("Block is to be created first\n")
                else:
                    login_account = random.randint(3001, acc_number - 1)
                    print(
                        f"\nAccountNo {login_account} found out the Nonce first!\nAccountNo {login_account} is mining the block\n"
                    )
                    skey = acc.userInfo[login_account]["secretkey"]
                    chal = auth.generate_challenge()
                    print(f"\nRandom challenge: {chal}")
                    rbit = auth.generate_randomBit()
                    print(f"Random bit: {rbit}")
                    msghmac = auth.create_response(skey, rbit, chal, login_account)
                    print(f"Response HMAC digest: {msghmac[1]}")
                    if verif[0]:
                        print("Calculated HMAC matched with received response!")
                        blkmsg = blk.mineBlock(login_account, time.time())
                        print(blkmsg)
                    else:
                        print("pasjndf allabsd msidilasdb")

    elif choice == "7":
        ch = input(
            "\n1: View Blockchain\n2: View Transactions (verified/unverified)\nSelect action: "
        )
        if ch == "2":
            print("\nVerified TransactionID List: ")
            for i in blk.verifiedTransac:
                print(blk.verifiedTransac[i])
            for i in blk.blockchainedTransac:
                print(blk.blockchainedTransac[i])
            if len(blk.verifiedTransac) + len(blk.blockchainedTransac) == 0:
                print("NA\n")
            print("\nUnverified TransactionID List: ")
            for i in blk.pendingTranac:
                print(blk.pendingTranac[i])
            if len(blk.pendingTranac) == 0:
                print("NA\n")
        elif ch == "1":
            for i in blk.chain:
                print(blk.printBlock(i))

    elif choice == "8":
        print("\nVIEW USER TRANSACTIONS")
        print("AccountNo. list: ")
        for i in acc.userInfo:
            print(i)
        login_account = int(input("Enter Account Number: "))
        if login_account in acc.userInfo:
            acc.viewUser(login_account)
        else:
            print("Invalid Account Number\n")
    elif choice == "9":
        print("\nVIEW USER DETAILS")
        print("AccountNo. list: ")
        for i in acc.userInfo:
            print(i)
        login_account = int(input("Enter Account Number: "))
        if login_account in acc.userInfo:
            nam = acc.userInfo[login_account]["name"]
            bal = acc.userInfo[login_account]["balance"]
            print(f"Name: {nam}\nBalance: {bal}")
            acc.viewUser(login_account)
    else:
        print("\nInvalid choice\n\n")
