from settings import W3

def verify_message(message, sign, account):
    W3.eth.account.recover_message(message, signature=sign)