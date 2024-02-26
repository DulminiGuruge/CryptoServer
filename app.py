from flask import Flask, jsonify, request
from bitcoin import *
from hashlib import sha256
import time

app = Flask(__name__)

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
    nonce=nonce+1
    if hash.startswith(prefix_str):
      print("Bitcoin mined with nonce value :",nonce)
      return hash, nonce
  print("Could not find a hash in the given range of upto", MAX_NONCE)




@app.route('/greeting', methods=['GET'])
def mining_machine():
  
#   group_id = request.args.get('group_id')
#   transactions = request.args.get('transactions')
#   difficulty = request.args.get('difficulty')
#   block_number = request.args.get('block_number')
#   previous_hash = request.args.get('previous_hash')
  
  group_id = 'A'
  transactions = '0->A->5 A->B->10 B->C->5 B->C->5'
  difficulty = '2'
  block_number = '2'
  previous_hash = '000000000000000000006bd3d6ef94d8a01de84e171d3553534783b128f06aad'
  
  

  print("Group ID")
  #group_id = input()
  coinbase= f'0->{group_id}->5 '
  print("provide the transaction list(as a string)")
  #transactions = input()
  transactions = coinbase + transactions
  #"."
  #684260
  print('what is the current level of difficulty?')
  #difficulty = input()
  difficulty = int(difficulty)
  import time as t
  begin=t.time()
  #previous_hash=input('previous hash: ')
  print('block number: ')
  #block_number =input()
  block_number = int(block_number)
  new_hash, nonce = mine(block_number ,transactions,previous_hash,difficulty)

  time_taken=t.time()- begin
  print("The mining process took ",time_taken,"seconds")

  print('=================================================================')
  print('\n                          Block header                         ')
  print('-----------------------------------------------------------------')

  print(f'Current block Number: {block_number}')
  print("New Block Hash:")
  print(new_hash)
  print('previous block hash:')
  print(previous_hash)
  print('Nonce:')
  print(nonce)
  print('-----------------------------------------------------------------')
  print('\n                          Block Content                        ')
  print('-----------------------------------------------------------------')

  print('confirmed transaction list:')
  print(transactions)
  print('=================================================================')
  app.logger.info("get identity response %s", transactions)

  return jsonify(transactions), 200
  #return jsonify(message=f"Done!")


@app.route('/greet', methods=['GET'])
def greet():
    mining_machine()
    
    
    return jsonify(message=f"Hello!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7655, debug=False)