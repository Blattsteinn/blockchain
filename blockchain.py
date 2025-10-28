

import hash #from hash.py

import datetime
import random

AMOUNT_OF_USERS = 1000
AMOUNT_OF_TRANSACTIONS = 1000

def create_users(amount: int):
    users = [User() for _ in range(amount)]
    users_dict = {user.public_key: user for user in users}
    print(f"[1] Created {amount} users")
    return users, users_dict

def create_transactions(amount: int, user_list):
    transactions = []
    for _ in range(amount):
        sender, receiver = random.sample(user_list, 2)
        currency_send = random.randint(1, 1000) * 50
        transactions.append(Transaction(sender.public_key, receiver.public_key, currency_send))

    print(f"[2] Created {amount} transactions")
    return transactions


used_names = {}
def get_random_name():
    names = ["Alice", "Bob", "Charlie", "Diana", "Edward", "Fiona", "George", "Hannah"]
    name = random.choice(names)

    # Check if it’s already used
    if name not in used_names:
        used_names[name] = 0
        return name
    else:
        used_names[name] += 1
        return f"{name}_{used_names[name]}"

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
        self.public_key = hash.hash_function(self.__private_key)

        self.balance = []
        self.balance.append(random.randrange(100, 1_000_000, 5))

    def add(self, amount):
        self.balance.append(amount)

    def spend(self, amount, sender):
        self.balance.sort()
        total: int = 0
        to_spend = []

        for part in self.balance:
            total += part
            to_spend.append(part)
            if total >= amount:
                break

        # if not enough:
        if total < amount:
            return

        for part in to_spend:
            self.balance.remove(part)

        change = total - amount
        if change > 0:
            self.balance.append(change)

        sender.add(amount)

    def __repr__(self):
        return(
            f"{self.name[:5]} has: {self.balance} \n"
        )

#Account model, switch to UTXO later
class Transaction:
    def __init__(self, sender_key: str, recipient_key: str, amount: int):
        self.transaction_id = hash.hash_function(sender_key + recipient_key + str(amount))

        self.sender = sender_key
        self.receiver = recipient_key
        self.amount = amount

    def __repr__(self):
        pass

class Block:
    def __init__(self, previous_hash, transactions, number = None):
        self.block_hash = None
        #------- Header
        self.previous_block_hash = self.previous_block_hash = previous_hash or "0" * 64
        self.timestamp = datetime.datetime.now()
        self.version = "v0.1"
        self.merkel_root_hash = self.merkle_root(transactions)
        self.nonce = 0
        self.difficulty_target = 3
        #-------- Transactions
        self.transactions = transactions
        #-------- Additional information
        self.mined = False
        self.number = number
        self.hash_start = "0" * self.difficulty_target

    # This is for print(Block)
    def __repr__(self):
        return (
            f"Block {self.number}(\n"
            f"  block_hash={self.block_hash},\n"
            f"  previous_block_hash={self.previous_block_hash},\n"
            f"  timestamp={self.timestamp},\n"
            f"  version={self.version},\n"
            f"  merkel_root_hash={self.merkel_root_hash},\n"
            f"  nonce={self.nonce},\n"
            f"  difficulty_target={self.difficulty_target},\n"
            f"  mined={self.mined},\n"
            f")\n"
        )

    def merkle_root(self, transactions):
        return hash.hash_function(".".join(_.transaction_id for _ in transactions))

    def mine_block(self):
        if self.mined:
            print("Is already mined")
            return

        header = f"{self.version}{self.timestamp}{self.previous_block_hash}{self.merkel_root_hash}{self.difficulty_target}"
        while True:
            current_guess = hash.hash_function(header + str(self.nonce))
            if current_guess.startswith(self.hash_start):
                self.block_hash = current_guess
                self.mined = True
                break
            self.nonce +=1

class Blockchain:
    def __init__(self):
        self.blocks = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis = Block(previous_hash=None, transactions=[], number = 0)
        genesis.mine_block()
        self.blocks.append(genesis)
        print("Genesis block created")

    def add_new_block(self, block):
        self.blocks.append(block)



def main():
    blockchain = Blockchain()

    # 1) Create 1000 users   -----------------------------------------------------------------------------/
    users, users_dict = create_users(amount = AMOUNT_OF_USERS)

    # 2) Generate 10,000 transaction -------------------------------------------------------------------/
    transactions = create_transactions(amount= AMOUNT_OF_TRANSACTIONS, user_list= users)

    amount_of_blocks = int(len(transactions)/100)
    for i in range(amount_of_blocks):
        print(f"{i+1}---------------------------------------------------")

        random_transactions = random.sample(transactions,100) # Step 3)
        previous_hash = blockchain.blocks[-1].block_hash
        block = Block(previous_hash = previous_hash, transactions = random_transactions, number = i + 1)
        block.mine_block() # Step 4) Mining the block
        print("Mined a block")

        # 5) Confirm the block and add it to the blockchain
        random_transactions_set = set(random_transactions)
        transactions = [trx for trx in transactions if trx not in random_transactions_set]
        for trx in random_transactions:
            sender_user= users_dict[trx.sender]
            receiver_user = users_dict[trx.receiver]
            sender_user.spend(trx.amount, receiver_user)

        blockchain.add_new_block(block)
        print("[5] Confirmed a block & removed transactions from the list")



    with open("all_blocks.txt.txt", 'w') as block_file:
        for block in blockchain.blocks:
            block_file.write(str(block))
        print("saved in .txt file")

    with open("users.txt", 'w') as user_file:
        for user in users:
            user_file.write(str(user))
        print("saved in .txt file")


if __name__ == "__main__":
    main()