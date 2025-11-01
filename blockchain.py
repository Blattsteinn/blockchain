import datetime
import json
from hash import hash_function
from typing import Dict, List



class Blockchain:
    def __init__(self):
        self.blocks = []

    def create_genesis_block(self):
        genesis = Block(previous_hash=None, transactions=[], number = 0)
        genesis.mine_block()
        self.blocks.append(genesis)
        print("Genesis block created")

    def add_new_block(self, block):
        self.blocks.append(block)
        print(f"[!] Added a new block #{block.block_number}")

    def validate_block_chain(self, transactions):
        # Validate if transaction hashes in the block match
        count: int = 0
        for block in self.blocks:
            if not block.merkle_tree() == block.merkle_root_hash:
                return False

            if block.validate_transactions(transactions):
                count += 1

        if not count == len(self.blocks):
            return False

        return True
class Block:
    def __init__(self, previous_hash, transactions, number = None):
        self.transactions = transactions
        self.block_hash = None
        self.block_number = number
        #------- Header
        self.previous_block_hash =  previous_hash or "0" * 64
        self.timestamp = datetime.datetime.now()
        self.version = "v0.1"
        self.merkle_root_hash = None #Should call after all trx have been confirmed: #self.merkle_tree()
        self.nonce = 0
        self.difficulty_target = 1
        #-------- Additional information
        self.amount_of_transactions = None
        self.mined =  False

        self.hash_start = "0" * self.difficulty_target

    def __repr__(self):
        return json.dumps({
            "block_number": self.block_number,
            "block_hash": self.block_hash,
            "previous_block_hash": self.previous_block_hash,
            "timestamp": str(self.timestamp),
            "version": self.version,
            "merkle_root_hash": self.merkle_root_hash,
            "nonce": self.nonce,
            "difficulty_target": self.difficulty_target,
            "amount_of_transactions": self.amount_of_transactions,
            "mined": self.mined,
            "transactions": self.transactions
        }, indent=2)

    @classmethod
    def read_from_file(cls, data):
        block = object.__new__(cls)

        block.transactions = data["transactions"]
        block.block_number = data["block_number"]
        block.block_hash = data["block_hash"]
        # ------- Header
        block.previous_block_hash = data['previous_block_hash']
        block.timestamp = data['timestamp']
        block.version = data["version"]
        block.merkle_root_hash = data["merkle_root_hash"]
        block.nonce = data["nonce"]
        block.difficulty_target = data["difficulty_target"]
        # -------- Additional information
        block.amount_of_transactions = data["amount_of_transactions"]
        block.mined = data["mined"]
        block.everything_valid = True
        # --------
        block.hash_start = "0" * block.difficulty_target
        return block

    def merkle_tree(self):
        if not self.transactions:
            return None

        current_list = self.transactions
        hash_list = []

        while True:

            if len(current_list) == 2:
                hashed_trx = hash_function(current_list[0] + current_list[1])
                return hashed_trx

            if len(current_list) % 2 == 1:
                current_list.append(current_list[-1])

            size = len(current_list)
            for i in range(0, size, 2):
                hashed_trx = hash_function(current_list[i] + current_list[i + 1])
                hash_list.append(hashed_trx)

            current_list = hash_list.copy()
            hash_list.clear()

    def mine_block(self):
        if self.mined:
            print("[!] Is already mined")
            return

        header = f"{self.version}{self.timestamp}{self.previous_block_hash}{self.merkle_root_hash}{self.difficulty_target}"
        while True:
            current_guess = hash_function(header + str(self.nonce))
            if current_guess.startswith(self.hash_start):
                self.block_hash = current_guess
                self.mined = True
                break
            self.nonce +=1
        print("[!] Mined a block")

    def validate_transactions(self, transactions: Dict):
        for t in self.transactions:
            trx_class = transactions[t]
            expected_hash = hash_function(trx_class.sender + trx_class.receiver + str(trx_class.amount))
            actual_hash = t

            if expected_hash != actual_hash:
                print(f"{actual_hash} is tampered")
                return False
        return True

    def remove_unvalid_transactions(self, transactions: Dict, users: Dict):
        for txid in self.transactions[:]: #[:] yra kaip .copy() wow
            trx_class = transactions[txid]
            sender, receiver = users[trx_class.sender], users[trx_class.receiver]

            if not sender.spend(trx_class.amount, receiver): #will return true or false
                self.transactions.remove(txid)
                del transactions[txid]
                print(f"[!!!] Bad transaction {txid}")
            else:
                trx_class.block_number = self.block_number

        self.amount_of_transactions = len(self.transactions)
        self.merkle_root_hash = self.merkle_tree() #Now compute a merkle_tree


