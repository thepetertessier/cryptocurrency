import utils
from datetime import datetime

def transfer_funds(src_wallet_file, dest_wallet_tag, amount, record_file):
    '''
    Transfer funds (`transfer`): this is how we pay with our cryptocurrency. It will be provided
    with four additional command line parameters: the source wallet file name (not the address!),
    the destination wallet tag (not the file name!), the amount to transfer, and the file name to
    save the transaction statement to. Any reasonable format for the transaction statement is
    fine for this, as long as the transaction statement is text and thus readable by a human.
    Recall that the transaction statement must have five pieces of information, described above
    in the “Transaction statement versus transaction line” section. Note that this command does
    NOT add anything to the mempool; it only writes the transaction statement. All transferred
    amounts are integers; we are not using floating-point numbers in this assignment at all.

    Example usage: `python3 cmoney.py transfer alice.wallet.txt <tagb> 12 03-alice-to-bob.txt`
    In this example, `<tagb>` would be the result of the address command, above, for Bob's wallet
    Example output: `Transferred 12 from alice.wallet.txt to d96b71971fbeec39 and the statement to '03-alice-to-bob.txt' on Tue Apr 02 23:09:00 EDT 2019`
    For this command, also, the exact output does not matter as long as it contains that information on one line
    '''
    src_pubkey, src_privkey = utils.loadWallet(src_wallet_file)
    src_wallet_tag = utils.get_tag(src_pubkey)
    date = utils.get_date_now()

    utils.make_transaction_statement(src=src_wallet_tag, dest=dest_wallet_tag, amount=amount, date=date, record_file=record_file)
    utils.add_signature_to_transaction_statement(record_file, src_privkey)
    print(f'Transferred {amount} from {src_wallet_file} to {dest_wallet_tag} and the statement to \'{record_file}\' on {date}')
