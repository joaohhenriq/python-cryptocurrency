import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse

class Blockchain:
    # inicializa a blockchain
    def __init__(self):
        # array de blocos
        self.chain = []
        # array de transações que serão utilizadas nos blocos
        self.transactions = []
        # já cria o primeiro bloco
        self.create_block(proof = 1, previous_hash = '0')
        # cria os vários nós de uma rede, usando o set em vez de array, pq set não deixa repetir itens, e por ser melhor pra trabalhar com nós
        self.nodes = set()
        
    # método para criar um bloco no array
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1, 
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transactions': self.transactions}
        
        # adicionamos a transação no bloco, e logo em seguida limpamos a lista pra receber novas transações
        self.transactions = []
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
    
    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount})
        
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1
    
    def add_node(self, address):
        # faz o parse do endereço (algo do tipo: http://127.0.0.1:5000) de rede do nó, fica algo assim
        # ParseResult(scheme='http', netloc='127.0.0.1:5000', path='/', ...)
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
        
    # protocolo de consenso: verifica todos os blockchains (nós) da rede, identifica o que tem mais blocos, e substitui os outros o blockchain dos outros nós por esse
    # com isso a gente garante que sempre todos os nós estarão em conformidade uns com os outros
    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        
        if longest_chain: #verifica se o atributo tá vazio
            self.chain = longest_chain
            return True
        return False
            

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


node_address = str(uuid4()).replace('-', '')




blockchain = Blockchain()

@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(sender = node_address, receiver = 'Node 5001', amount=1)
    
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'You ve mine a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'transactions': block['transactions']}
    
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


@app.route('/add_transaction', methods = ['POST'])
def add_transaction():
    json = request.get_json()
    transactions_keys = ['sender', 'receiver', 'amount']
    if not all(key in json for key in transactions_keys):
        return 'You have some missing elements', 400
    
    index = blockchain.add_transaction(json['sender'], json['receiver'], json['amount'])
    response = {'message': f'Transaction add to block {index}'}
    return jsonify(response),201


@app.route('/conect_node', methods = ['POST'])
def conect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return 'Empty nodes...', 400
    
    for node in nodes:
        blockchain.add_node(node)
        
    response = {'message': 'Nodes connected. Blockchain have these nodes: ',
                'total_nodes': list(blockchain.nodes)}
    return jsonify(response), 201


@app.route('/replace_chain', methods = ['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message': 'Nodes updated',
                 'new_chain': blockchain.chain}
    else:
        response = {'message': 'No actions needed...',
                 'actual_chain': blockchain.chain}
    
    return jsonify(response), 201
        
    
    

app.run(host = '0.0.0.0', port = 5001)

























    