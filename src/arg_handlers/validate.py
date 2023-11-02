import os
import utils

def validate_all_blocks():
    '''
    Validate the blockchain (`validate`): this should go through the entire block chain,
    validating each block. This means that starting with block 1 (the block after the
    genesis block), ensure that the hash listed in that file, which is the hash for the
    previous block file, is correct. The only thing you must check with this is that the
    the previous hash values are all valid; we are not checking balances for this. The
    blockchain is considered valid if only the genesis block exists. However, we will
    never call this function if the genesis block has not been created. Thus, you don't
    have to actually check if the genesis block exists, as we will never call validate
    on it if it does not exist. Likewise, you don't have to do any checks on the genesis
    block file itself. There are no additional command-line parameters for this function.

    NOTE: this should ONLY print either 'True' or 'False' (if it's valid or not), and
    nothing else! Case matters here.

    Example usage: `python3 cmoney.py validate`
    Example output: `True` or `False`
    '''
    expected_hash = utils.hashFile(utils.BLOCKS_DIR + 'block_0.txt')
    for block_file in os.listdir(utils.BLOCKS_DIR)[1:]:
        with open(utils.BLOCKS_DIR + block_file, 'r') as file:
            written_hash = file.readline().strip()
        if written_hash != expected_hash:
            print(False)
            return
    print(True)
