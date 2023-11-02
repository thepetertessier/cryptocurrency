import utils, rsa

def create_wallet(wallet_file):
    '''
    Generate a wallet (`generate`): this will create RSA public/private key set (1024 bit
    keys is appropriate for this assignment). The resulting wallet file MUST BE TEXT -
    you will have to convert any binary data to text to save it (and convert it in the
    other direction when loading). You can see the provided helper functions, above, to
    help with this. The file name to save the wallet to will be provided as an additional
    command line parameter.

    Example usage: `python3 cmoney.py generate alice.wallet.txt`
    Example output: `New wallet generated in 'alice.wallet.txt' with tag e1f3ec14abcb45da`
    For this command, also, the exact output does not matter as long as it contains that
    information on one line (with or without the tag)
    '''
    path = utils.WALLETS_DIR + wallet_file
    pubkey, privkey = rsa.newkeys(1024)
    utils.saveWallet(pubkey, privkey, path)
    tag = utils.get_tag(pubkey)
    print('New wallet generated in \'%s\' with tag %s' % (path, tag))
    