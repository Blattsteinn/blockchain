
import hash #from hash.py
from blockchain import Blockchain, Block
import json
import random
import time

AMOUNT_OF_USERS = 100
AMOUNT_OF_TRANSACTIONS = 1000
used_names = {}

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

def get_random_name():
    names = ["Alice", "Bob", "Charlie", "Diana", "Edward", "Fiona", "George", "Hannah"]
    name = random.choice(names)

    if name not in used_names:
        used_names[name] = 0
        return name
    else:
        used_names[name] += 1
        return f"{name}_{used_names[name]}"

def get_private_key():
    list_of_characters = [1, 2, 3, 4, 5, 6, 7, 8, 9, 'A', 'B', 'C', 'D', 'E', 'F', 0]
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

    def __repr__(self):
        return json.dumps( {
            "name": self.name,
            "private_key": self.__private_key,
            "public_key": self.public_key,
            "balance": self.balance
        }, indent=2)

    @classmethod
    def read_from_file(cls, data):
        user = object.__new__(cls)

        user.name = data["name"]
        user.__private_key = data["private_key"]
        user.public_key = data["public_key"]
        user.balance = data["balance"]

        return user

    def add(self, amount):
        self.balance.append(amount)

    def spend(self, amount, receiver):
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

        receiver.add(amount)


class Transaction:
    def __init__(self, sender_key: str, recipient_key: str, amount: int, number: int = None):
        self.transaction_id = hash.hash_function(sender_key + recipient_key + str(amount))
        self.sender = sender_key
        self.receiver = recipient_key
        self.amount = amount
        self.block_number = number

    @classmethod
    def read_from_file(cls, id, data):
        transaction = object.__new__(cls)

        transaction.transaction_id = id
        transaction.sender = data["sender"]
        transaction.receiver = data["receiver"]
        transaction.amount = data["amount"]
        transaction.block_number = data["block_number"]

        return transaction

    def __repr__(self):
        return json.dumps( {
        f"{self.transaction_id}": {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "block_number": self.block_number
            }
        }, indent=2)

def main():
    with open("transactions.txt", 'w') as f: pass
    with open("all_blocks.txt", 'w') as f: pass
    with open("users.txt", 'w') as f: pass
    blockchain = Blockchain()
    blockchain.create_genesis_block()


    #print("Generate 100 users")
    #print("Create 100 random transactions")

    # Create 1000 users   -----------------------------------------------------------------------------
    users, users_dict = create_users(amount = AMOUNT_OF_USERS)

    # Generate 10,000 transaction ---------------------------------------------------------------------
    transactions = create_transactions(amount= AMOUNT_OF_TRANSACTIONS, user_list= users)

    amount_of_blocks = int(len(transactions)/100)

    all_transactions = []
    for idx in range(amount_of_blocks):
        random_transactions = random.sample(transactions,100) # Step 3)
        previous_hash = blockchain.blocks[-1].block_hash

        id_list = [trx.transaction_id for trx in random_transactions]
        block = Block(previous_hash = previous_hash, transactions = id_list, number = idx + 1)

        block.mine_block()
        print(f"Mined a block {idx}")

        # Confirm the block and add it to the blockchain ------------------------------------------------
        random_transactions_set = set(random_transactions)
        for trx in transactions:
            if trx in random_transactions_set:
                trx.block_number = idx + 1

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

        all_transactions.extend(random_transactions)

        blockchain.add_new_block(block)
        print("[3] Confirmed a block & removed transactions from the list")

    write_to_files(all_transactions, blockchain, users)

def write_to_files(all_transactions, blockchain, users):
    # ------------ Transactions
    with open("transactions.txt", 'w') as f:
        f.write(f"[\n")
        for i, trx in enumerate(all_transactions):
            f.write(str(trx))
            if i < len(all_transactions) - 1:
                f.write(",\n")
            else:
                f.write("\n")
        f.write(f"]\n")

    # ------------ Blocks
    with open("all_blocks.txt", 'w') as f:
        f.write(f"[\n")

        for i, block in enumerate(blockchain.blocks):
            f.write(str(block))
            if i < len(blockchain.blocks) - 1:
                f.write(",\n")
            else:
                f.write("\n")

        f.write(f"]\n")
    # ------------ Users
    with open("users.txt", 'w') as f:
        f.write(f"[\n")
        for i, user in enumerate(users):
            f.write(str(user))
            if i < len(users) - 1:
                f.write(",\n")
            else:
                f.write("\n")
        f.write(f"]\n")

def import_from_files():
    #-------- Blocks
    blockchain = Blockchain()
    with open('all_blocks.txt', 'r') as f:
        block_from_file = json.load(f)

    for b in block_from_file:
        block = Block.read_from_file(b)
        blockchain.blocks.append(block)

    #--------- Users
    users = []
    with open("users.txt", "r") as f:
        users_from_file = json.load(f)

    for u in users_from_file:
        user = User.read_from_file(u)
        users.append(user)

    # --------- Transactions
    transactions = {}
    with open("transactions.txt", "r") as f:
        transactions_from_file = json.load(f)

    for t in transactions_from_file:
        trx_id = next(iter(t.keys()))
        trx_data = t[trx_id]

        transaction = Transaction.read_from_file(trx_id, trx_data)
        transactions[trx_id] = transaction


    return blockchain, users, transactions




if __name__ == "__main__":
    #main()

    # Import data from existing files
    blockchain, users, transactions = import_from_files()
    users_dict = {user.public_key: user for user in users}
    transactions_list = list(transactions.values())

    # Validate if transaction hashes in the block match match
    if blockchain.validate_block_chain(transactions):
        print("[!] All transactions are valid")
    else: print("[!] There are invalid transactions")

    while True:
        x = input("Generate 100 transactions? ")
        if x == "n":
            break

        new_transactions = create_transactions(100, users)
        new_id_list = [trx.transaction_id for trx in new_transactions]
        transactions

        block = Block(previous_hash=blockchain.blocks[-1].block_hash, transactions=new_id_list,
                      number = blockchain.blocks[-1].block_number + 1)
        block.mine_block()
        blockchain.add_new_block(block)

        transactions_list.extend(new_transactions)

        print("[!] Added a new block")

    # End program
    write_to_files(transactions_list, blockchain, users)
    print("Successfully saved")



        # y = input("TRX ID?")
        # print(transactions[y].sender_key)

    # while True:
    #     x = int(input("Select block info to print out: "))
    #     print(blockchain.blocks[x])
    #
    #     x = int(input("Select user info to print out: "))
    #     print(users[x])
    #
    #     x = int(input("Select block number to print all trx "))
    #     print(blockchain.blocks[x].transactions)