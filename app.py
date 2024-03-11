from flask import Flask, jsonify, request
from bitcoin import *
from hashlib import sha256
import time
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

MAX_NONCE=10000000


def SHA256(text):
  return sha256(text.encode("ascii")).hexdigest()


def mine(block_number,transaction,previous_hash,prefix_zeros):
  prefix_str='0'*prefix_zeros
  nonce=0
  while(1):
    time.sleep(0.005)
    text= str(block_number) + transaction + previous_hash + str(nonce)
    #print(text)
    hash = SHA256(text)
    # print(hash)
    nonce= random.randint(1, 100000) #nonce+1
    if hash.startswith(prefix_str):
      print("Bitcoin mined with nonce value :",nonce)
      return hash, nonce
  print("Could not find a hash in the given range of upto", MAX_NONCE)




@app.route('/startmining', methods=['POST'])
def mining_machine():
  
  group_id = str(request.form.get('group_id'))
  transactions = str(request.form.get('transactions'))
  difficulty = request.form.get('difficulty')
  block_number = request.form.get('block_number')
  previous_hash = str(request.form.get('previous_hash'))

  print('id:'+group_id+',transaction:'+transactions+",difficulity:"+str(difficulty)+",blockno"+str(block_number)+",prev hash"+previous_hash)
  
  #group_id = 'A'
  #transactions = '0->A->5 A->B->10 B->C->5 B->C->5'
  #difficulty = '2'
  #block_number = '2'
  #previous_hash = '000000000000000000006bd3d6ef94d8a01de84e171d3553534783b128f06aad'
  
  

  coinbase= f'0->{group_id}->5 '
 
  transactions = coinbase + transactions

  

  if difficulty is not None:
      try:
          app.logger.info(difficulty)
          difficulty = int(difficulty)
          # Use group_id_int as an integer
      except ValueError:
          # Handle the case where group_id is not a valid integer
          print("Invalid difficulty value. Must be an integer.")
  else:
      # Handle the case where group_id is None
      difficulty = 2

      print("difficulty parameter is missing in the request.")
  

  import time as t
  begin=t.time()

  if block_number is not None:
      try:
          app.logger.info(block_number)
          block_number = int(block_number)
          # Use group_id_int as an integer
      except ValueError:
          # Handle the case where group_id is not a valid integer
          print("Invalid block_number value. Must be an integer.")
  else:
      # Handle the case where group_id is None
      block_number = 2

      print("block_number parameter is missing in the request.")
  
  new_hash, nonce = mine(block_number ,transactions,previous_hash,difficulty)

  time_taken=t.time()- begin
  
  print("The mining process took ",time_taken,"seconds")

  

  result = {
        "Current block Number": block_number,
        "New Block Hash": new_hash,
        "previous block hash": previous_hash,
        "Nonce": nonce,
        "Transactions": transactions
  }

  app.logger.info("Mining result: %s", result)

  return jsonify(result), 200
  #return jsonify(message=f"Done!")


@app.route('/validateblocks', methods=['POST'])
def block_validator():

#   input transaction list
# 0->A->5 A->B->10 B->C->5 B->C->5
# Block Number:
# 2
# Previous hash:
# 000000000000000000006bd3d6ef94d8a01de84e171d3553534783b128f06aad
# nonce:
# 440
# Hash of the new block:
# 0018b090a6039a44a2b094489321548e7b20f3a0a56ba8020f988d864d637069
# Current Dificulty:
# 2


  vtransaction_list = str(request.form.get('vtransaction_list'))
  vblock_no = request.form.get('vblock_no')
  vprev_hash = str(request.form.get('vprev_hash'))
  vnonce = request.form.get('vnonce')
  vnew_hash = str(request.form.get('vnew_hash'))
  vdifficulity = request.form.get('vdifficulity')

  nonce = int(vnonce) -1
  nonce = str(nonce)


  Dificulty = int(vdifficulity)
  block_result = ""
  hash_result = ""
  try:
    int(vnew_hash[:Dificulty])
    block_result += " New block meets the difficulty requirment \n"
  except:
    block_result += "block is not valid not enough leading zeros \n"


  text= str(vblock_no) + vtransaction_list + vprev_hash + str(nonce)
  #print(text)
  hash = SHA256(text)
  if hash == vnew_hash:
    hash_result += 'New hash value is valid! \n'
  else:
    hash_result += 'given nonce does not produce the above hash \n'

  
  

  result = {
        "block_result": block_result,
        "hash_result": hash_result
  }

  app.logger.info("Validation Result result: %s", result)

  return jsonify(result), 200
  #return jsonify(message=f"Done!")


@app.route('/greet', methods=['GET'])
def greet():
    mining_machine()
    
    
    return jsonify(message=f"Hello!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7655, debug=False)