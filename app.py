from flask import Flask, jsonify, request
from hashlib import sha256
import time
from flask_cors import CORS
import random
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

executor = ThreadPoolExecutor(max_workers=10)  # Handle up to 10 parallel requests
MAX_NONCE = 10000000

def SHA256(text):
    """Returns the SHA-256 hash of the given text."""
    return sha256(text.encode("ascii")).hexdigest()

def mine(block_number, transaction, previous_hash, prefix_zeros):
    """Mining function to find a hash with leading zeros."""
    prefix_str = '0' * prefix_zeros
    nonce = 0
    while True:
        time.sleep(0.005)  # To prevent high CPU usage
        text = str(block_number) + transaction + previous_hash + str(nonce)
        hash_value = SHA256(text)
        
        if hash_value.startswith(prefix_str):
            print("Bitcoin mined with nonce value:", nonce)
            return hash_value, nonce
        else: 
            nonce = random.randint(1, 100000)  # Random nonce value

@app.route('/startmining', methods=['POST'])
def mining_machine():
    """API endpoint to start mining asynchronously."""
    try:
        group_id = str(request.form.get('group_id', ''))
        transactions = str(request.form.get('transactions', ''))
        difficulty = request.form.get('difficulty')
        block_number = request.form.get('block_number')
        previous_hash = str(request.form.get('previous_hash', ''))

         # Validate inputs
        try:
            difficulty = int(difficulty) if difficulty else 2
            #block_number = int(block_number) if block_number else 2
        except ValueError:
            return jsonify({"error": "Invalid difficulty or block_number value. Must be integers."}), 400




        coinbase = f'0->{group_id}->5 '
        transactions = coinbase + transactions

        # Run mining asynchronously
        future = executor.submit(mine, block_number, transactions, previous_hash, difficulty)
        new_hash, nonce = future.result()
        time_taken = future.done()

        result = {
            "Current Block Number": block_number,
            "New Block Hash": new_hash,
            "Previous Block Hash": previous_hash,
            "Nonce": nonce,
            "Transactions": transactions,
            "Time Taken (seconds)": time_taken
        }

        app.logger.info("Mining result: %s", result)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@app.route('/validateblocks', methods=['POST'])
def block_validator():
    """API endpoint to validate blocks asynchronously."""
    try:
        vtransaction_list = str(request.form.get('vtransaction_list', ''))
        vblock_no = request.form.get('vblock_no')
        vprev_hash = str(request.form.get('vprev_hash', ''))
        vnonce = request.form.get('vnonce')
        vnew_hash = str(request.form.get('vnew_hash', ''))
        vdifficulty = request.form.get('vdifficulty')

        # Validate inputs
        try:
            nonce = int(vnonce) - 1
            difficulty = int(vdifficulty)
        except (ValueError, TypeError):
            return jsonify({"error": "Invalid nonce or difficulty value. Must be integers."}), 400

        block_result = ""
        hash_result = ""

        if vnew_hash.startswith('0' * difficulty):
            block_result += "New block meets the difficulty requirement.\n"
        else:
            block_result += "Block is not valid; not enough leading zeros.\n"

        # Validate the hash
        text = str(vblock_no) + vtransaction_list + vprev_hash + str(nonce)
        calculated_hash = SHA256(text)
        if calculated_hash == vnew_hash:
            hash_result += 'New hash value is valid!\n'
        else:
            hash_result += 'Given nonce does not produce the expected hash.\n'

        result = {
            "block_result": block_result,
            "hash_result": hash_result
        }

        app.logger.info("Validation Result: %s", result)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@app.route('/greet', methods=['GET'])
def greet():
    """Simple greeting endpoint."""
    return jsonify(message="Hello!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7655, threaded=True, debug=False)
