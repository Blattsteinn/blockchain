import hash #from hash.py
from blockchain import Blockchain, Block

import random

AMOUNT_OF_USERS = 1000
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

    # Check if it’s already used
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

    def __repr__(self):
        return f"{self.name:<12} has: {self.balance}\n"

class Transaction:
    def __init__(self, sender_key: str, recipient_key: str, amount: int):
        self.transaction_id = hash.hash_function(sender_key + recipient_key + str(amount))
        self.sender = sender_key
        self.receiver = recipient_key
        self.amount = amount

    def __repr__(self):
        return f"{self.sender} sent {self.amount:<8} to {self.receiver}\n"

def main():
    with open("transactions.txt", 'w') as f: pass
    with open("all_blocks.txt", 'w') as f: pass
    with open("users.txt", 'w') as f: pass
    blockchain = Blockchain()

    # Create 1000 users   -----------------------------------------------------------------------------
    users, users_dict = create_users(amount = AMOUNT_OF_USERS)

    # Generate 10,000 transaction ---------------------------------------------------------------------
    transactions = create_transactions(amount= AMOUNT_OF_TRANSACTIONS, user_list= users)

    amount_of_blocks = int(len(transactions)/100)

    for i in range(amount_of_blocks):
        random_transactions = random.sample(transactions,100) # Step 3)
        previous_hash = blockchain.blocks[-1].block_hash
        block = Block(previous_hash = previous_hash, transactions = random_transactions, number = i + 1)

        block.mine_block()
        print(f"Mined a block {i}")

        # Confirm the block and add it to the blockchain ------------------------------------------------
        random_transactions_set = set(random_transactions)
        transactions = [trx for trx in transactions if trx not in random_transactions_set]

        valid_transactions = []
        for index, trx in enumerate(random_transactions):
            sender_user= users_dict[trx.sender]
            receiver_user = users_dict[trx.receiver]

            sender_balance = sum(sender_user.balance)
            if sender_balance < trx.amount:
                print("mhh")
                continue
            valid_transactions.append(trx)
            sender_user.spend(trx.amount, receiver_user)

        with open("transactions.txt", 'a') as transaction_file:
            transaction_file.write(f"------------------------------------------------------\n")
            transaction_file.write(f"Block [{i}]\n")
            for index, trx in enumerate(valid_transactions):
                transaction_file.write(f"{index} {trx}")

        blockchain.add_new_block(block)
        print("[5] Confirmed a block & removed transactions from the list")


    with open("all_blocks.txt", 'w') as block_file:
        for block in blockchain.blocks:
            block_file.write(str(block))
        print("saved in all_blocks.txt file")

    with open("users.txt", 'w') as user_file:
        for user in users:
            user_file.write(str(user))
        print("saved in users.txt file")


if __name__ == "__main__":
    main()