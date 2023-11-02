from datetime import datetime
import utils

def fund_wallet(wallet_tag, amount, record_file):
    '''
    Fund wallets (`fund`): this allows us to add as much money as we want to a wallet.
    While this is obviously not practical in the real world, it will allow us to test
    your program. (Although there still needs to be a way to fund wallets in the real
    world also). Create a special case ID ('bigfoot', 'daddy_warbucks', 'lotto',
    'satoshi_nakamoto', or whatever) that your program knows to use as the source for
    a fund request, and also knows not to verify when handling verification, below.
    This means that 'bigfoot' (or whatever) will appear alongside the hash of the
    public keys as the source of funds. This function will be provided with three
    additional command line parameters: the destination wallet tag, the amount to
    transfer, and the file name to save the transaction statement to. All funded
    amounts are integers; we are not using floating-point numbers in this assignment
    at all.

    Example usage: `python3 cmoney.py fund <taga> 100 01-alice-funding.txt`
    In this example, <taga> is the result of the address command, above, for Alice's wallet
    Example output: `Funded wallet d96b71971fbeec39 with 100 AaronDollars on Tue Apr 02 23:09:00 EDT 2019`
    For this command, also, the exact output does not matter as long as it contains that information on one line
    '''
    date = utils.get_date_now()
    print('record_file',record_file)
    utils.make_transaction_statement(src=utils.BIG_FUNDER, dest=wallet_tag, amount=amount, date=date, record_file=record_file)
    print(f'Funded wallet {wallet_tag} with {amount} {utils.CRYPTO_NAME}s on {date}')
