
import json
import time
from hashlib import sha256


class Block:

    def __init__(self, index, transactions, timestamp, previous_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()


class Blockchain:

    difficulty = 2

    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), '0'*64)
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    def print_block(self, n):
        if len(self.chain) < n:
            return
        else:
            block = self.chain[n]
            return f'Index: {block.index}\nTransactions: {block.transactions}\nTimestamp: {block.timestamp}\nPrevious hash: {block.previous_hash}'

    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()

        while not computed_hash.startswith('0'*.Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash





a = Blockchain()
print(a.print_block(0))

    

