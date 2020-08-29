
import json
import time
from hashlib import sha256
from flask import Flask, request
import requests


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
        while not computed_hash.startswith('0'*Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def add_block(self, block, proof):
        previous_hash = self.last_block.hash
        if previous_hash != block.previous_hash:
            return False
        if not self.is_valid_proof(block, proof):
            return False
        block.hash = proof
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash):
        return (block_hash.startswith('0'*Blockchain.difficulty) and block_hash == block.compute_hash())

    def new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def mine(self):
        if not self.unconfirmed_transactions:
            return False
        last_block = self.last_block
        new_block = Block(index=last_block.index-1, transactions=self.unconfirmed_transactions, timestamp=time.time(), previous_hash=last_block.hash)
        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = []
        return new_block.index

# #- prueba
# a = Blockchain()
# a.new_transaction('tran1 sdfsdfs')
# a.new_transaction('tran2 hjdtn')
# a.mine()
# len_bc = len(a.chain)
# print(a.print_block(len_bc-1))


app = Flask(__name__)
blockchain = Blockchain()

@app.route('/new_transaction', methods['POST'])
    def new_transaction():
        tx_data = request.get_json()
        require_fields = ["author", "content"]

        for field in require_fields:
            if not tx_data.get(field):
                return 'Datos de transaccion invalidos', 404

        tx_data["timestamp"] = time.time()
        blockchain.new_transaction(tx_data)
        return 'Exito', 201



