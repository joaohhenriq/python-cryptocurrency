import datetime
import hashlib
import json
from flask import Flask, jsonify

class Blockchain:
    # inicializa a blockchain
    def __init__(self):
        self.chain = []
        # já cria o primeiro bloco
        self.create_block(proof = 1, previous_hash = '0')
        
    # método para criar um bloco no array
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1, 
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash}
        
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            # cria o desafio que tem que ser atingido para liberar a criação de um novo bloco na cadeia
            hash_operation = hashlib.sha256(str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            
            # nesse caso, o algoritmo pede que seja um número que comece com 0000
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
            
        return new_proof
    
    # transforma o bloco em json e gera o hash dele
    def hash(self, block):
        #transforma o bloco em json
        encoded_block = json.dumps(block, sort_keys=True).encode()
        
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            
            # verifica se o previous hash do bloco atual é diferente do anterior a ele
            # se for, então a validação é falsa
            if block['previous_hash'] != self.hash(previous_block):
                return False
            
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            
            previous_block = block
            block_index += 1
            
        return True
            

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

blockchain = Blockchain()

@app.route('/get_mine_block', methods = ['GET'])
def get_mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Youve mine a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    
    return jsonify(response), 200


@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    
    return jsonify(response), 200
            

@app.route('/is_valid', methods = ['GET'])
def is_valid():
    response = {'is_valid': blockchain.is_chain_valid(blockchain.chain)}
    
    return jsonify(response), 200


app.run(host = '0.0.0.0', port = 5000)




    