

import hash

#python libraries
import datetime
import random

def get_random_name():
    names = ["Alice", "Bob", "Charlie", "Diana", "Edward", "Fiona", "George", "Hannah"]
    return random.choice(names)

def get_private_key():
    list_of_characters = [1,2,3,4,5,6,7,8,9,'A','B','C','D','E','F',0]
    hex_string = ""
    for _ in range(64):
        hex_string += str(random.choice(list_of_characters)).lower()
    return hex_string


class User:
    def __init__(self):
        self.name = get_random_name()
        self.__private_key = get_private_key()
        self.public_key = hash.hash_function(self.__private_key) #for simplicity

        self.balance = random.randrange(100, 1_000_000, 5)

    def add(self, _amount):
        self.balance += _amount


#Account model, switch to UTXO later
class Transaction:
    def __init__(self, _sender_key: str, recipient_key: str, _amount: int):
        self.transaction_id = hash.hash_function(_sender_key + recipient_key + str(_amount))
        self.sender = _sender_key
        self.receiver = recipient_key
        self.amount = _amount

class Block:
    def __init__(self, previous_hash, _transactions):

        # Block Header
        self.previous_block_hash = previous_hash
        self.timestamp = datetime.datetime.now()
        self.version = "v0.1"
        if _transactions is None:
            self.merkel_root_hash = hash.hash_function("None")
        else:
            self.merkel_root_hash = hash.hash_function(".".join(_.transaction_id for _ in _transactions)) # Just hash all transactions for now
        self.nonce = 0
        self.difficulty_target = 3

        self.block_hash = None
        self.mined = False
        self.number = None
        self.transactions = _transactions

    def __repr__(self):
        return (
            f"Block(\n"
            f"  previous_block_hash={self.previous_block_hash},\n"
            f"  timestamp={self.timestamp},\n"
            f"  version={self.version},\n"
            f"  merkel_root_hash={self.merkel_root_hash},\n"
            f"  nonce={self.nonce},\n"
            f"  difficulty_target={self.difficulty_target},\n"
            f"  block_hash={self.block_hash},\n"
            f"  mined={self.mined},\n"
            f")"
        )

    def mine_block(self):
        if self.mined:
            print("Is already mined")
            return

        hash_start = "0" * self.difficulty_target

        header = f"{self.version}{self.timestamp}{self.previous_block_hash}{self.merkel_root_hash}{self.difficulty_target}"

        while True:
            current_guess = header + str(self.nonce)
            self.block_hash = hash.hash_function(current_guess)

            if self.block_hash.startswith(hash_start):
                self.mined = True
                break
            else:
                self.nonce +=1

class Blockchain:
    def __init__(self):
        self.blocks = []

    def create_genesis_block(self):
        genesis = Block(previous_hash=None, _transactions=None)
        genesis.mine_block()
        print("Genesis created")
        self.blocks.append(genesis)

    def add_new_block(self, _block):
        self.blocks.append(_block)

if __name__ == "__main__":

    blockchain = Blockchain()
    blockchain.create_genesis_block()

    # 1) Create 1000 users
    users = [User() for _ in range(25)]
    users_dict = {user.public_key: user for user in users}
    print("Created 1000 users")

    # 2) Generate 10,000 transaction
    transactions = []
    for _ in range(10_00):
        while True:
            sender = random.choice(users)
            receiver = random.choice(users)

            if sender != receiver:
                amount = random.randint(1, 20) * 5

                if sender.balance >= amount:
                    break

        transactions.append(Transaction(sender.public_key, receiver.public_key, amount))
    print("Created 10_00 transactions")

    for _ in range(2):

        # 3) Choosing 100 random transactions
        random_transactions = []
        for _ in range(100):
            transaction = random.choice(transactions)
            random_transactions.append(transaction)
        print("Picked 100 random transactions")

        # 4) Mine the block
        _previous_hash = blockchain.blocks[-1].block_hash
        block = Block(previous_hash=_previous_hash, _transactions = random_transactions)
        block.mine_block()
        print("Mined a block")


        # 5) Confirm the block and add it to the blockchain
        transactions = [trx for trx in transactions if trx not in random_transactions]
        for trx in random_transactions:
            users_dict[trx.sender].add(-trx.amount)
            users_dict[trx.receiver].add(trx.amount)
        blockchain.add_new_block(block)
        print("Confirmed a block & added transactions")

        #


    for block in blockchain.blocks:
        print(block)