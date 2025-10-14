import hash
import datetime

class User:
    def __init__(self, name):
        self.name = name
        self.public_key = None #this is hash?
        self.__private_key = None#this is hash?
        self.balance = None

class Transaction:
    #utxo model here??
    def __init__(self, sender_key: str, recipient_key: str, amount: float):
        self.transaction_id = None #this is some sort of hash
        self.sender = sender_key
        self.receiver = recipient_key
        self.amount = amount

class Block:
    def __init__(self, previous_hash):
        self.previous_block_hash = previous_hash
        self.timestamp = datetime.datetime.now()
        self.version = "v0.1"
        self.merkel_root_hash = None#???
        self.nonce = 0 #???
        self.difficulty_target = 1#???

class Blockchain:
    def __init__(self):
        self.chain = []

if __name__ == "__main__":
    
    user_input: int

    while True:
        word = input("Enter the word you want to hash: ")
        hash_received = hash.hash_function(word)
        print(f"Word: {word[:20]}, hash: {hash_received}")