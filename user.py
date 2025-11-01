import random
import json
from typing import List, Dict

from hash import hash_function

used_names = {}

class User:
    def __init__(self):
        self.name = get_random_name()
        self.__private_key = get_private_key()
        self.public_key = hash_function(self.__private_key)

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

    def spend(self, amount, receiver) -> bool:
        self.balance.sort()

        total: int = sum(self.balance)

        if total < amount:   # If not enough:
            return False

        to_spend = []
        total = 0
        for part in self.balance:
            total += part
            to_spend.append(part)
            if total >= amount:
                break

        for part in to_spend:
            self.balance.remove(part)

        change = total - amount
        if change > 0:
            self.balance.append(change)

        receiver.add(amount)

        return True


def create_users(amount: int):
    users = [User() for _ in range(amount)]
    users_dict = {user.public_key: user for user in users}
    print(f"/--- Created {amount} users ---/")
    return users, users_dict

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
