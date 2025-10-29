# Blockchain

This repository showcases simple blockchain implementation using Python that tries to simulate real life scenarios.

## Usage
1. Navigate to the folder you want to clone the repository and run:

```git clone https://github.com/Blattsteinn/blockchain.git```

2. Open the project folder in your IDE and open ```main.py``` OR navigate to the project folder and run ```python main.py``` via command prompt
3. In the IDE run the script
```python
if __name__ == "__main__":
    main()
```
For faster results, consider changing variable at the top of ```main.py```
```python
AMOUNT_OF_USERS = 10
AMOUNT_OF_TRANSACTIONS = 500
```
You can also reduce the difficulty level for faster mining.
```python
class Block:
    def __init__(self, previous_hash, transactions, number = None):
        self.block_hash = None
        #------- Header
        self.difficulty_target = 1 # <---- Here
```

## Blockchain & block structure
```blockchain.py```
```python
class Blockchain:
    def __init__(self):
        self.blocks = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis = Block(previous_hash=None, transactions=[], number = 0)
        genesis.mine_block()
        self.blocks.append(genesis)

    def add_new_block(self, block):
        self.blocks.append(block)
```
```python
class Block:
    def __init__(self, previous_hash, transactions, number = None):
        self.block_hash = None
        #------- Header
        self.previous_block_hash = self.previous_block_hash = previous_hash or "0" * 64
        self.timestamp = datetime.datetime.now()
        self.version = "v0.1"
        self.merkel_root_hash = self.merkle_root()
        self.nonce = 0
        self.difficulty_target = 3
        #-------- Transactions
        self.transactions = transactions
        #-------- Additional information
        self.mined = False
        self.number = number
        self.hash_start = "0" * self.difficulty_target
```
## Explanation
```main.py```

**1)** Firstly we initialize a blockchain, which creates a genesis block.
```python
blockchain = Blockchain()
```

**2)** Then we generate 1000 users with a starting balance of 100 - 1,000,000 and 10,000 transactions.
```python
AMOUNT_OF_USERS = 1000
AMOUNT_OF_TRANSACTIONS = 10_000

    users, users_dict = create_users(amount = AMOUNT_OF_USERS)
    transactions = create_transactions(amount= AMOUNT_OF_TRANSACTIONS, user_list= users)
```
User balance here is stored using UTXO model. 

```python
class User:
    def __init__(self):
        self.name = get_random_name()
        self.__private_key = get_private_key()
        self.public_key = hash.hash_function(self.__private_key)

        self.balance = []
        self.balance.append(random.randrange(100, 1_000_000, 5))
```
```python
class Transaction:
    def __init__(self, sender_key: str, recipient_key: str, amount: int):
        self.transaction_id = hash.hash_function(sender_key + recipient_key + str(amount))

        self.sender = sender_key
        self.receiver = recipient_key
        self.amount = amount
```
***Note***: ```hash_function``` comes from hash.py


**3)** Pick 100 random transactions, fetch previous block hash, create a new block and start mining it.
```python
        random_transactions = random.sample(transactions,100)
        previous_hash = blockchain.blocks[-1].block_hash
        block = Block(previous_hash = previous_hash, transactions = random_transactions, number = i + 1)
        block.mine_block()
```
When the block is mined we remove the randomly picked transactions from the transaction list, update the user balance and add the the block to the blockchain.

```python
        random_transactions_set = set(random_transactions)
        transactions = [trx for trx in transactions if trx not in random_transactions_set]

        valid_transactions = []
        for index, trx in enumerate(random_transactions):
            sender_user= users_dict[trx.sender]
            receiver_user = users_dict[trx.receiver]

            sender_balance = sum(sender_user.balance)
            if sender_balance < trx.amount:
                print("Unsufficient funds")
                continue
            valid_transactions.append(trx)
            sender_user.spend(trx.amount, receiver_user)
```

and we repeat this part till there's no transactions left.

## Results
Results can be seen in ```users.txt```, ```all_blocks.txt```, ```transactions.txt```

Snippet when we finish mining 100 blocks: 
<img width="931" height="560" alt="image" src="https://github.com/user-attachments/assets/e047f8ff-1cf3-4d3e-93ce-e3130c4ec3e0" />
