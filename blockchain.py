import datetime
from hash import hash_function

class Block:
    def __init__(self, previous_hash, transactions, number = None):
        self.block_hash = None
        #------- Header
        self.previous_block_hash =  previous_hash or "0" * 64
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
        self.amount_of_transactions = len(transactions)

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
            f" amount_of_transactions={self.amount_of_transactions},\n"
            f"  mined={self.mined},\n"
            f")\n"
        )

    def merkle_root(self, transactions):
        return hash_function(".".join(_.transaction_id for _ in transactions))

    def mine_block(self):
        if self.mined:
            print("Is already mined")
            return

        header = f"{self.version}{self.timestamp}{self.previous_block_hash}{self.merkel_root_hash}{self.difficulty_target}"
        while True:
            current_guess = hash_function(header + str(self.nonce))
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