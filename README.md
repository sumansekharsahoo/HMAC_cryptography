# NET BANKING SYSTEM

This is a secure net banking system developed using blockchain technology. It provides features like user registration, deposit, withdrawal, transfer of funds, transaction verification, block creation and mining, and viewing the blockchain and transaction history.

## Features

- **User Registration**: Register a new user with an account number, secret key, and initial deposit amount.
- **Deposit**: Deposit funds into an existing account after authentication using the secret key and HMAC challenge-response mechanism.
- **Withdrawal**: Withdraw funds from an existing account after authentication using the secret key and HMAC challenge-response mechanism.
- **Transfer**: Transfer funds from one account to another after authentication using the secret key and HMAC challenge-response mechanism.
- **Transaction Verification**: Verify individual or all unverified transactions using the account's secret key.
- **Block Creation**: Create a new block by combining verified transactions into a Merkle tree.
- **Block Mining**: Simulate the mining process where nodes compete to find the nonce and mine the created block.
- **View Blockchain**: View the entire blockchain, including all mined blocks and their details.
- **View Transactions**: View verified, unverified, and blockchain-included transactions.
- **View User Transactions**: View all transactions performed by a specific user account.
- **View User Details**: View the name, balance, and transaction history of a specific user account.

## Technologies Used

- Python
- Cryptographic libraries (hmac, hashlib)
- Random number generation
- Data structures (lists, dictionaries)

### `Account` Class

This class represents a user account in the banking system.

#### Methods

- `__init__(self)`: Initializes an empty dictionary to store user information, a list to store secret keys, and a dictionary to store transactions.
- `generateSecretKey(self)`: Generates a random 5-character secret key using uppercase letters.
- `viewUser(self, accno)`: Prints the transactions performed by the given account number.

### `Auth` Class

This class handles authentication mechanisms using HMAC and challenge-response.

#### Methods

- `generate_challenge(self)`: Generates a random challenge message of length between 8 and 12 bits.
- `generate_randomBit(self)`: Generates a random bit (0 or 1).
- `create_response(self, secret_key, rbit, challenge, amt)`: Creates an HMAC response using the given secret key, random bit, challenge, and amount.
- `verify_response(self, secret_key, rbit, challenge, hmac_res, amt)`: Verifies the HMAC response against the calculated HMAC value using the given secret key, random bit, challenge, and amount.

### `Blockchain` Class

This class represents the blockchain and handles block creation, mining, and transaction verification.

#### Methods

- `__init__(self)`: Initializes dictionaries to store verified, pending, and blockchain-included transactions, a list to store the blockchain, and a list to store unmined blocks.
- `initiategenesisblock(self, timestmp)`: Creates and prints the genesis block of the blockchain.
- `addUnverifiedTransaction(self, timestamp, transaction, tid)`: Adds an unverified transaction to the pending transactions dictionary.
- `verifytransaction(self, transac_id, accno, skey, auth, acc)`: Verifies a transaction using the provided account number, secret key, and authentication mechanism.
- `merkletree(self, t1, t2, t3)`: Constructs a Merkle tree from three transactions and returns the root hash.
- `createBlock(self, blkproducer)`: Creates a new block with verified transactions and adds it to the list of unmined blocks.
- `printBlock(self, blk_dict)`: Returns a formatted string representation of a block.
- `mineBlock(self, blkminer, tstamp)`: Simulates the mining process by mining the first unmined block with the given miner account and timestamp.
