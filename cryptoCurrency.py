import hashlib, json
from datetime import datetime, timedelta

class Block:
    def __init__(self, data):
        self.data = data
        self.prev_hash = ""
        self.nonce = 0
        self.hash = ""
        self.total_time = ""

def hash(block):
    data = json.dumps(block.data) + block.prev_hash + str(block.nonce)
    data = data.encode('utf-8')
    return hashlib.sha256(data).hexdigest()

# block = Block("Bui Tran Anh Tri + Coder")
# print(hash(block))

class Blockchain:
    def __init__(self, owner):
        self.owner = owner
        self.chain = []

        block = Block("Genesis Block")
        block.hash = hash(block)

        self.chain.append(block)

    def add_block(self, data):
        block = Block(data)
        block.data.append({"from":"", "to": self.owner, "amount": 1000})
        block.prev_hash = self.chain[-1].hash
        block.hash = hash(block)
        start = datetime.now()
        while hash(block).startswith("00") == False:
            block.nonce = block.nonce + 1  
            block.hash = hash(block)
        end = datetime.now()
        block.total_time = str(end-start)

        self.chain.append(block)

    def print(self):
        for block in self.chain:
            print("")
            print("Data:", block.data)
            print("Previous hash:", block.prev_hash)
            print("Hash:", block.hash)
            print("Nonce:", block.nonce)
            print("Total time:", block.total_time)
            print("")

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            prev_block = self.chain[i-1]

            if hash(current_block) != current_block.hash:
                return False
            
            if prev_block.hash != current_block.prev_hash:
                return False

        return True
    
    def get_balance(self, person):
        balance = 0
        for block in self.chain:
            if type(block.data) != list:
                continue
            for transfer in block.data:
                if transfer["from"] == person:
                    balance = balance - transfer["amount"]
                if transfer["to"] == person:
                    balance = balance + transfer["amount"]
        return balance

    
blockchain = Blockchain("Gabriel Belmont")
blockchain.add_block([
    {"from": "Bui Tran Anh Tri", "to": "Gabriel Belmont","amount":1000},
    {"from": "Gabriel Belmont", "to": "Dracula","amount":100},
    {"from": "Gabriel Belmont", "to": "Alucard","amount":200}
])
blockchain.add_block([
    {"from": "Gabriel Belmont", "to": "Dracula","amount":50},
    {"from": "Gabriel Belmont", "to": "Alucard","amount":50}
    
])

print("Balance of Gabriel Belmont:", blockchain.get_balance("Gabriel Belmont"), "TriCoin")
blockchain.print()