import utils

def get_wallet_address(wallet_file):
    '''
    Get wallet tag (`address`): this will print out the tag of the public key for a given
    wallet, which is likely the first 16 (or so) characters of the SHA-256 hash of the
    public key. Note that it only prints out that tag (no other output). When the other
    commands talk about naming a wallet, this is what it actually means. You are welcome
    to use the first 16 characters of the hash of the public key for this assignment; you
    don't need to use the entire hash. The file name of the wallet file will be provided
    as an additional command line parameter. To avoid confusion with the signatures
    discussed elsewhere, we will call the this the wallet's tag or address.

    Example usage: `python3 cmoney.py address alice.wallet.txt`
    Example output: `e1f3ec14abcb45da`, or whatever that wallet's tag is - note that
    NOTHING ELSE should be printed, just the wallet tag
    '''
    path = utils.WALLETS_DIR + wallet_file
    pubkey, privkey = utils.loadWallet(path)
    print(utils.get_tag(pubkey))
