import arg_handlers.name as name
import arg_handlers.genesis as genesis
import arg_handlers.generate as generate
import arg_handlers.address as address
import arg_handlers.fund as fund
import arg_handlers.transfer as transfer
import arg_handlers.balance as balance
import arg_handlers.verify as verify
import arg_handlers.mine as mine
import arg_handlers.validate as validate

def handle_args(argv):
    arg = argv[1]

    if arg == 'name':
        name.print_name()

    elif arg == 'genesis':
        genesis.create_block_0()
    
    elif arg == 'generate':
        wallet_file = argv[2]
        generate.create_wallet(wallet_file)
    
    elif arg == 'address':
        wallet_file = argv[2]
        address.get_wallet_address(wallet_file)
    
    elif arg == 'fund':
        wallet_tag, amount, record_file = argv[2:]
        fund.fund_wallet(wallet_tag, amount, record_file)

    elif arg == 'transfer':
        src_wallet_file, dest_wallet_tag, amount, record_file = argv[2:]
        transfer.transfer_funds(src_wallet_file, dest_wallet_tag, amount, record_file)

    elif arg == 'balance':
        wallet_tag = argv[2]
        balance.print_balance(wallet_tag)

    elif arg == 'verify':
        wallet_file, record_file = argv[2:]
        verify.verify_transaction_and_add_to_mempool(wallet_file, record_file)

    elif arg == 'mine':
        difficulty = argv[2]
        mine.move_transactions_to_new_block(difficulty)

    elif arg == 'validate':
        validate.validate_all_blocks()

    else:
        raise Exception('Unrecognized argument \'%s\'' % arg)
