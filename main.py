
import hash
from blockchain import Blockchain, Block
from user import User, create_users
from transaction import Transaction, create_transactions

from typing import List, Dict
import json
import random
import time

AMOUNT_OF_USERS = 100
AMOUNT_OF_TRANSACTIONS = 1000

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

def reset():
    #This resets the blockchain, generates 100 blocks with random transactions in them
    with open("transactions.txt", 'w') as f: pass
    with open("all_blocks.txt", 'w') as f: pass
    with open("users.txt", 'w') as f: pass
    blockchain = Blockchain()
    blockchain.create_genesis_block()

    # Create 1000 users
    users, users_dict = create_users(amount = AMOUNT_OF_USERS)
    # Generate 10,000 transaction
    transactions, transactions_dict = create_transactions(amount= AMOUNT_OF_TRANSACTIONS, user_list= users)

    valid_transactions = []
    amount_of_blocks = int(len(transactions) / 100)
    for i in range(0, AMOUNT_OF_TRANSACTIONS, 100):
        temporary_transactions = transactions[i:(i+100)]

        previous_hash = blockchain.blocks[-1].block_hash

        id_list = [trx.transaction_id for trx in temporary_transactions]
        block = Block(previous_hash = previous_hash, transactions = id_list, number = blockchain.blocks[-1].block_number + 1)

        block.remove_unvalid_transactions(transactions_dict, users_dict)
        for trx in block.transactions:
            if trx in transactions_dict:
                valid_transactions.append(transactions_dict[trx])

        block.mine_block()
        blockchain.add_new_block(block)
        print(f"Mined a block {blockchain.blocks[-1].block_number}")


    write_to_files(valid_transactions, blockchain, users)


def new_main():
    # Import data from existing files
    blockchain, users, transactions = import_from_files()
    users_dict = {user.public_key: user for user in users}
    transactions_list = list(transactions.values())

    # Validate if transaction hashes in the block match match
    if blockchain.validate_block_chain(transactions):
        print("[!] All transactions are valid")
    else: print("[!] There are invalid transactions")

    while True:
        x = input("Command: ")
        choice = x.split()
        if x.lower() == "n" or x.lower() == "exit":
            break

        if choice[0] == "mine":

            print("/--- Creating 100 transactions and mining a block ---/")
            new_transactions, transactions_dict = create_transactions(100, users)
            new_id_list = [trx.transaction_id for trx in new_transactions]

            block = Block(previous_hash=blockchain.blocks[-1].block_hash, transactions=new_id_list,
                          number = blockchain.blocks[-1].block_number + 1)

            block.remove_unvalid_transactions(transactions_dict, users_dict)
            block.mine_block()
            blockchain.add_new_block(block)
            transactions_list.extend(new_transactions)

        elif choice[0] == "block":
            print(blockchain.blocks[int(choice[1])])

        elif choice[0] == "trx":
            print(transactions[choice[1]])


    # End program
    write_to_files(transactions_list, blockchain, users)
    print("Successfully saved")

if __name__ == "__main__":
    #reset()
    new_main()
