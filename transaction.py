import random
import json
from typing import List, Dict

from hash import hash_function

class Transaction:
    def __init__(self, sender_key: str, recipient_key: str, amount: int,  sender_private_key: str, number: int = None,):
        self.transaction_id = hash_function(sender_key + recipient_key + str(amount))
        self.signature = hash_function(sender_private_key + recipient_key + str(amount))
        self.sender = sender_key
        self.receiver = recipient_key
        self.amount = amount
        self.block_number = number

    @classmethod
    def read_from_file(cls, txid, data):
        transaction = object.__new__(cls)

        transaction.transaction_id = txid
        transaction.signature = data["signature"]
        transaction.sender = data["sender"]
        transaction.receiver = data["receiver"]
        transaction.amount = data["amount"]
        transaction.block_number = data["block_number"]

        return transaction

    def __repr__(self):
        return json.dumps( {
        f"{self.transaction_id}": {
            "signature": self.signature,
            "sender": self.sender,
             "receiver": self.receiver,
             "amount": self.amount,
             "block_number": self.block_number
            }
        }, indent=2)

def create_transactions(amount: int, user_list):
    transactions = []
    for _ in range(amount):
        sender, receiver = random.sample(user_list, 2)
        currency_send = random.randint(1, 1000) * 50
        transactions.append(Transaction(sender.public_key, receiver.public_key, currency_send, sender._User__private_key))

    print(f"/--- Created {amount} transactions ---/")
    transactions_dict = {}
    for tx in transactions:
        transactions_dict[tx.transaction_id] = tx

    return transactions, transactions_dict
