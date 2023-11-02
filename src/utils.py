'''DO NOT import any other files from this project!'''

import hashlib
import binascii
import rsa
import os
from datetime import datetime

# Constants
CRYPTO_NAME = 'MoneyCoin'
WALLETS_DIR = 'wallets/'
BLOCKS_DIR = 'blocks/'
TRANSACTIONS_DIR = 'transactions/'
BIG_FUNDER = 'Papa Peter'
MEMPOOL_FILE = 'mempool.txt'

def get_date_now():
    return str(datetime.now().strftime("%a %b %d %H:%M:%S EDT %Y"))

def get_joined_file_lines(filename, start=0, end=None):
    with open(filename, 'r') as file:
        lines = file.readlines()[start:] if end == None else file.readlines()[start:end]
    return ''.join(lines)

def get_hash(byte):
    h = hashlib.sha256()
    h.update(byte)
    return h.hexdigest()

# gets the hash of a file; from https://stackoverflow.com/a/44873382
def hashFile(filename):
    h = hashlib.sha256()
    with open(filename, 'rb', buffering=0) as f:
        for b in iter(lambda : f.read(128*1024), b''):
            h.update(b)
    return h.hexdigest()

# given an array of bytes, return a hex reprenstation of it
def bytesToString(data):
    return binascii.hexlify(data)

# given a hex reprensetation, convert it to an array of bytes
def stringToBytes(hexstr):
    return binascii.a2b_hex(hexstr)

def namespace(filename, directory):
    if not filename.startswith(directory):
        return directory + filename
    return filename

# Load the wallet keys from a filename
def loadWallet(filename):
    filename = namespace(filename, WALLETS_DIR)
    with open(filename, mode='rb') as file:
        keydata = file.read()
    privkey = rsa.PrivateKey.load_pkcs1(keydata)
    pubkey = rsa.PublicKey.load_pkcs1(keydata)
    return pubkey, privkey

# save the wallet to a file
def saveWallet(pubkey, privkey, filename):
    filename = namespace(filename, WALLETS_DIR)
    # Save the keys to a key format (outputs bytes)
    pubkeyBytes = pubkey.save_pkcs1(format='PEM')
    privkeyBytes = privkey.save_pkcs1(format='PEM')
    # Convert those bytes to strings to write to a file (gibberish, but a string...)
    pubkeyString = pubkeyBytes.decode('ascii')
    privkeyString = privkeyBytes.decode('ascii')
    # Write both keys to the wallet file
    with open(filename, 'w') as file:
        file.write(pubkeyString)
        file.write(privkeyString)
    return

def get_tag(pubkey):
    return hex(pubkey.n)[2:18]

def get_next_file_no(directory):
    transaction_files = os.listdir(directory)
    if not transaction_files:
        return 0
    last = sorted(transaction_files)[-1]
    last_no = last.split('_')[1].split('.')[0]
    return int(last_no) + 1

def make_transaction_statement(src, dest, amount, date=get_date_now(), record_file=None, signature=None):
    if record_file == None:
        record_file = 'transaction_' + str(get_next_file_no(TRANSACTIONS_DIR))
    with open(TRANSACTIONS_DIR + record_file, 'w') as file:
        file.write('From: %s\n' % src)
        file.write('To: %s\n' % dest)
        file.write('Amount: %s\n' % amount)
        file.write('Date: %s' % date)
        if src != BIG_FUNDER and signature != None:
            file.write('\n\n%s' % signature)

def add_signature_to_transaction_statement(record_file, privkey):
    record_file = namespace(record_file, TRANSACTIONS_DIR)
    # transaction_hash = int(hashFile(record_file), 16)
    # signature = hex(privkey.blinded_encrypt(transaction_hash))[2:]
    message = get_joined_file_lines(record_file) + '\n'
    message = message.encode('ascii')
    signature = str(bytesToString(rsa.sign(message, privkey, 'SHA-256')))[2:-1]

    with open(record_file, 'a') as file:
        file.write(f'\n\n{signature}')

def get_transaction_line(src, dest, amount, date):
    return f'{src} transferred {amount} to {dest} on {date}'

def get_transaction_info_from_line(line):
    line, date = line.split(' on ')
    line, dest = line.split(' to ')
    src, amount = line.split(' transferred ')
    return src, int(amount), dest, date

def get_transaction_info_from_record_file(record_file):
    record_file = namespace(record_file, TRANSACTIONS_DIR)
    with open(record_file) as file:
        src = file.readline().strip()[6:]
        dest = file.readline().strip()[4:]
        amount = int(file.readline().strip()[8:])
        date = file.readline().strip()[6:]
    return src, dest, amount, date


def get_mempool_lines():
    with open(MEMPOOL_FILE, 'r') as file:
        return file.readlines()
    
def get_block_lines():
    block_lines = []
    for block_file in os.listdir(BLOCKS_DIR)[2:]:
        with open(BLOCKS_DIR + block_file, 'r') as file:
            block_lines.extend(file.readlines()[2:-2])
    return block_lines

def get_balance(wallet_tag):
    balance = 0

    for line in get_block_lines() + get_mempool_lines():
        src, amount, dest, date = get_transaction_info_from_line(line.strip())
        if src == wallet_tag:
            balance -= amount
        if dest == wallet_tag:
            balance += amount

    return balance
