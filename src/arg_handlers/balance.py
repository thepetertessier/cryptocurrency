import utils

def print_balance(wallet_tag):
    '''
    Check a balance (`balance`): based on the transactions in the block chain AND ALSO in the
    mempool, compute the balance for the provided wallet. This does not look at transaction
    statements, only the transaction lines in the blocks and the mempool. Thus, if a
    transaction has been written to a transaction statement file from the transfer command,
    but not moved into the mempool (via the `verify` command, next), then that transaction is
    NOT considered when computing the balance. But all transaction lines in the blocks of
    the blockchain and also the mempool are considered. The wallet address to compute the
    balance for is provided as an additional command line parameter.

    NOTE: this should ONLY print the balance as a number, as an integer, and nothing else!
    Example usage: `python3 cmoney.py balance <taga>`
    In this example, `<taga>` is the result of the `address` command, above, for Alice's wallet
    Example output: `90` - this should print NOTHING ELSE other than the (integer) balance
    '''
        
    print(utils.get_balance(wallet_tag))
