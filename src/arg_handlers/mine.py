import utils, hashlib

def remove_nonce(nonce, next_block):
    nonce_length = len(str(nonce))
    with open(next_block, 'r') as file:
        contents = file.read()
    with open(next_block, 'w') as file:
        file.write(contents[:-nonce_length])

def works_for_nonce(nonce, next_block, difficulty):
    with open(next_block, 'a') as file:
        file.write(str(nonce))

    file_hash = utils.hashFile(next_block)

    if file_hash[:difficulty] == '0'*difficulty:
        return True
    
    remove_nonce(nonce, next_block)
    return False

def wipe_mempool():
    with open(utils.MEMPOOL_FILE, 'w') as file:
        file.write('')

def move_transactions_to_new_block(difficulty):
    '''
    Create and mine the block (`mine`): this will form another block in the blockchain. The
    mempool will be emptied of transaction lines, as they will all go into the current
    block being computed. A nonce will have to be computed to ensure the hash is below a
    given value. Recall that the first line in any block is the SHA-256 of the last block
    file. The difficulty for the mining will be the additional parameter to this command.
    For simplicity, the difficulty will be the number of leading zeros to have in the hash
    value - so a value of 3 would imply that the hash must start with three leading zeros.
    We will be using very small difficulties here, so a brute-force method for finding the
    nonce is sufficient (just like in all other proof-of-work cryptocurrencies). A
    difficulty of 2 is appropriate for our tests. The nonce must be a single unsigned 32
    bit (or 64 bit) integer.

    Example usage: `python3 cmoney.py mine 2`
    Example output: Mempool transactions moved to `block_1.txt and mined with difficulty 2 and nonce 1029`
    For this command, also, the exact output does not matter as long as it contains that
    information on one line
    '''

    # h = hashlib.sha256()
    # with open(utils.MEMPOOL_FILE, 'rb', buffering=0) as f:
    #     for b in iter(lambda : f.read(128*1024), b''):
    #         h.update(b)
    
    # while h.hexdigest()[:difficulty] != '0'*difficulty:
    #     h.update()

    difficulty = int(difficulty)
    latest_block = utils.BLOCKS_DIR + 'block_' + str(utils.get_next_file_no(utils.BLOCKS_DIR)-1) + '.txt'
    next_block = utils.BLOCKS_DIR + 'block_' + str(utils.get_next_file_no(utils.BLOCKS_DIR)) + '.txt'
    with open(utils.MEMPOOL_FILE, 'r') as file:
        mempool = file.read()
    with open(next_block, 'w') as file:
        file.write(utils.hashFile(latest_block) + '\n\n' + mempool + '\n\nnonce: ')
    
    for nonce in range(10000):
        if works_for_nonce(nonce, next_block, difficulty):
            print(f'Mempool transactions moved to \'{next_block}\' and mined with difficulty {difficulty} and nonce {nonce}')
            wipe_mempool()
            return
    print('Could not find a nonce')
