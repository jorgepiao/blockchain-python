
import json
from hashlib import sha256


class Block:

    def __init__(self, index, transactions, timestamp):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp

    def compute_hash(block):
        block_string = json.dump(self.__dict__, sort=True)
        return sha256(block_string.encode()).hexdigest()

    

