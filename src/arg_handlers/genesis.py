import utils

def create_block_0():
    '''
    Create the genesis block (`genesis`): this is the initial block in the block chain,
    and the block should always be the same. Come up with a fun quote! It should always
    be written to a `block_0.txt` file. Only have one zero in there! We are going to
    check for the presence of `block_0.txt`, and thus `block_00.txt` will fail this test.
    There are no additional command line parameters to this function.

    Example usage: `python3 cmoney.py genesis`
    Example output: `Genesis block created in 'block_0.txt'`
    '''
    path = utils.BLOCKS_DIR + 'block_0.txt'
    with open(path, 'w') as block_0:
        block_0.write('Money, if it does not bring you happiness, will at least help you be miserable in comfort.')

    print('Genesis block created in \'%s\'' % path)
