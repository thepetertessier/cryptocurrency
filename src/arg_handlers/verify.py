import utils, rsa

def signature_is_valid(record_file, pubkey):
    with open(record_file, 'r') as file:
        signature = utils.stringToBytes(file.readlines()[-1].strip())
    message = utils.get_joined_file_lines(record_file, 0, -2)
    try:
        rsa.verify(message.encode('ascii'), signature, pubkey)
        return True
    except rsa.VerificationError:
        return False

def funds_are_available(src, amount, balance, wallet_tag):
    if src != wallet_tag:
        return True
    return balance >= amount

def add_to_mempool(transaction_line):
    empty = False
    with open(utils.MEMPOOL_FILE, 'r') as mempool:
        if mempool.read() == '':
            empty = True
    with open(utils.MEMPOOL_FILE, 'a') as mempool:
        if not empty:
            mempool.write('\n')
        mempool.write(transaction_line)

def verify_transaction_and_add_to_mempool(wallet_file, record_file):
    '''
    Verify a transaction (`verify`): verify that a given transaction statement is valid,
      which will require checking the signature and the availability of funds. For funds
      available, just use the result of the `balance` command, above. Once verified, it
      should be added to the mempool as a transaction line. This is the only way that
      transactions are added to the mempool. The wallet file name (whichever wallet
      created the transaction) and the transaction statement being verified are the
      additional command line parameters.

    Example usage: `python3 cmoney.py verify bob.wallet.txt 04-bob-to-alice.txt`
    Example output: `The transaction in file '04-bob-to-alice.txt' with wallet 'bob.wallet.txt' is valid, and was written to the mempool`
    For this command, also, the exact output does not matter as long as it contains that information on one line    
    '''
    record_file = utils.namespace(record_file, utils.TRANSACTIONS_DIR)
    src, dest, amount, date = utils.get_transaction_info_from_record_file(record_file)
    if src == utils.BIG_FUNDER:
        add_to_mempool(utils.get_transaction_line(src, dest, amount, date))
        print('Any funding request is considered valid; written to the mempool')
        return

    pubkey, privkey = utils.loadWallet(wallet_file)
    wallet_tag = utils.get_tag(pubkey)
    balance = utils.get_balance(utils.get_tag(pubkey))

    if not signature_is_valid(record_file, pubkey):
        print(f'Sorry, the transaction in file \'{record_file}\' with wallet \'{wallet_file}\' has an invalid signature, and was not written to the mempool')
    elif not funds_are_available(src, amount, balance, wallet_tag):
        print(f'Sorry, the wallet \'{wallet_file}\' has insufficient funds for the transaction file \'{record_file}\', and the transaction was not written to the mempool')
    else:
        add_to_mempool(utils.get_transaction_line(src, dest, amount, date))
        print(f'The transaction in file \'{record_file}\' with wallet \'{wallet_file}\' is valid, and was written to the mempool')
