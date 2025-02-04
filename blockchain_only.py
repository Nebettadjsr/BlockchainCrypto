# Module 1 - Create Blockchain

import datetime
import hashlib
import json
from flask import Flask, jsonify

######################## For Later use #################
# import oqs 

# # Select a Dilithium variant (e.g., "Dilithium2" is one common parameter set)
# algorithm = "Dilithium2"

# # Create a signature context
# with oqs.Signature(algorithm) as signer:
#     # Generate a keypair (the public and secret keys)
#     public_key = signer.generate_keypair()
    
#     # Example message to be signed (e.g., a transaction in your blockchain)
#     message = b"Transaction data: Alice pays Bob 10 coins"
    
#     # Create a signature on the message using the secret key
#     signature = signer.sign(message)
    
#     # Verification: using the public key, verify that the signature matches the message
#     is_valid = signer.verify(message, signature, public_key)
    
#     print("Signature valid:", is_valid)
############################################################

class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')
    
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain)+1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 
                 }
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha512(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self, block): #22. Step 7
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha512(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash']!= self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha512(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True

# create Web App
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Create Blockchain

blockchain = Blockchain()

# Mining a Block

@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Great!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                }
    return jsonify(response), 200

# Getting full Blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

#cheking if Blockchain is valid
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'All good! The Chain is valid' }
    else:
        response = {'message': 'Problem!'}
    return jsonify(response), 200

# running the app
app.run(host = '0.0.0.0', port= 5000)
