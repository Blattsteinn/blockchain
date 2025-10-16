from idlelib.pyparse import trans

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

        self.balance = random.randint(100,1000000)

    def add(self, _amount):
        self.balance += _amount



#Account model, switch to UTXO later
class Transaction:

    def __init__(self, sender_key: str, recipient_key: str, _amount: float):
        self.transaction_id = hash.hash_function(sender_key + recipient_key + str(amount))
        self.sender = sender_key
        self.receiver = recipient_key
        self.amount = _amount

class Block:
    def __init__(self, previous_hash, transactions):
        self.timestamp = datetime.datetime.now()

        self.previous_block_hash = previous_hash
        self.transaction_list = transactions
        self.block_hash = None # Here to hash transactions
        self.merkel_root_hash = None  #

        self.version = "v0.1"
        self.nonce = 0 #???
        self.difficulty_target = 1#???

class Blockchain:
    def __init__(self):
        self.chain = []

if __name__ == "__main__":

    # 1) Create 1000 users
    users = [User() for _ in range(1000)]

    # 2) Generate 10,000 transaction
    transactions = []
    for _ in range(10_000):
        sender = random.choice(users)
        receiver = random.choice(users)

        amount = random.randint(0, sender.balance)
        transactions = Transaction(sender, receiver, amount)
        sender.add(amount)
        receiver.add(-amount)

    # 3) Creating a block with 100 random transactions