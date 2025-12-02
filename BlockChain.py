import hashlib
import random

#the difficulty setting which is just the number of bits which are required
#to be leading 0s
DIFFICULTY = 24

#mine a block by finding a nonce that produces a hash with enough leading 0s
def mine_block(prev_hash, quote):    
    #converts the input into bytes
    prev_bytes = bytes.fromhex(prev_hash)
    quote_bytes = quote.encode('ascii')
    
    #calculates how many leading zero bytes are needed, by dividing by 8
    zero_bytes_needed = DIFFICULTY // 8
    
    attempts = 0
    while True:
        #picks a random 4 byte nonce
        nonce_int = random.randint(0, 2**32 - 1)
        nonce_bytes = nonce_int.to_bytes(4, 'big')
        
        #builds the block data and hashes it
        block_data = prev_bytes + nonce_bytes + quote_bytes
        result = hashlib.sha256(block_data).digest()
        
        #checks if there are enough leading zero bytes
        if all(result[i] == 0 for i in range(zero_bytes_needed)):
            result_hex = result.hex()
            return nonce_int, result_hex
        
        #keeps track of attempts just so i know the program has not stalled
        attempts += 1
        if attempts % 1000000 == 0:
            print(f"On attempt {attempts:,}")


#main function
def main():
    block_num = 1
    while True:
        print(f"On block: {block_num}\n")
        
        #grabs previous block's hash and quote
        prev_hash = input("Previous block hash (type 'quit' to exit program): ").strip()
        #allows out of the program without killing it with ctrl c
        if prev_hash.lower() == 'quit':
            break
            
        print(f"\n")

        quote = input("Quote (type 'retry' if hash was skipped on accident): ").strip()
        if quote.lower() == 'retry':
            continue
        
        print(f"\n")
        nonce, block_hash = mine_block(prev_hash, quote)
        
        print(f"\nResults:\n")
        print(f"  Nonce: {nonce}\n")
        print(f"  Hash:  {block_hash}\n")
        
        block_num += 1

#runs main
main()